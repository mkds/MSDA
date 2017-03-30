from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.filters import StaticAssets, Q500US, make_us_equity_universe, Q1500US
from quantopian.pipeline.data.morningstar import asset_classification, valuation
from itertools import combinations
import statsmodels.api as statm
from statsmodels.tsa.stattools import adfuller
import pandas as pd


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # Provide Universe from which stocks needs to be select
    context.universe = Q500US()
    # context.universe = StaticAssets([sid(5061),sid(3766)])
    # Max number of stocks to be considered for pairs
    context.population_size = 200
    # Max number of pairs
    context.max_pairs = 10
    # Window to do stationary testing
    context.stationary_window = 50
    # Initialize history of pairs
    context.pair_hist = {}
    # Track Pair postion
    context.pair_pos = []
    # Significance level for Co integration testing
    context.signi_level = 0.05
    # Deviation above which to trade (in sd terms)
    context.deviation_cutoff = 1.25
    # Cutoff at which to close the pair to realize profit
    context.close_cutoff = .25
    # Cutoff at which to close the pair to limit loss
    context.stop_loss = 3.1
    # Short-sale maintenance margin requirement 125%, i.e 25% more than the cash received from short sale
    context.margin = 0.25
    context.first_run = True

    # Rebalance every day, 1 hour after market open.
    schedule_function(trade_pairs, date_rules.every_day(), time_rules.market_open(hours=1))

    # Record tracking variables at the end of each day.
    schedule_function(track_status, date_rules.every_day(), time_rules.market_close())

    # Create our dynamic stock selector.
    attach_pipeline(pipeline_data(context), 'fund_data')


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.stock_list = pipeline_output('fund_data')
    context.stock_list.loc[:, "sid"] = context.stock_list.index
    context.today_pairs = []
    # print context.stock_list
    hist_price(context, data)
    # print "Total Pairs %s, coin pairs %s" %


def trade_pairs(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """

    # First check if we need to sell any current position
    # Get weights for pair which indicates how wide is the arbitrage
    # Also limit losses
    weight_pos = [get_weight(context, data, pair, context.close_cutoff, context.stop_loss) for pair in context.pair_pos]

    # Close pairs for which profit is already realized or close to cut loss
    for ind, weight in enumerate(weight_pos):
        if weight == 0:
            close_pair(context, data, context.pair_pos[ind])
    context.pair_pos = [pair for ind, pair in enumerate(context.pair_pos) if weight_pos[ind] != 0]

    # If the number of position less than max then get list of pairs
    #    to be evaluated for trading
    if len(context.pair_pos) == context.max_pairs:
        return
    else:
        get_pairs(context, data)

    # Order Amount for each trade
    value = context.portfolio.cash / context.max_pairs / context.margin
    rel_weights = []

    # Get pair weights which gives the possible upside value
    for pair in context.today_pairs:
        rel_weights.append(get_weight(context, data, pair, context.deviation_cutoff))

    # Get pairs with good profit potential. That is Sort paris by weight
    context.today_pairs = [b for a, b in sorted(zip(rel_weights, context.today_pairs),
                                                key=lambda x: abs(x[0]), reverse=True)]

    rel_weights.sort(key=lambda x: -abs(x))
    cur_pos = [sec.sid for stocks in context.pair_pos for sec in stocks]
    # Only consider stocks which are not already in portfolio
    for ind, pair in enumerate(context.today_pairs):
        if rel_weights[ind] != 0:
            if pair[0].sid in cur_pos or pair[1].sid in cur_pos:
                rel_weights[ind] = 0
            else:
                cur_pos.append(pair[0].sid)
                cur_pos.append(pair[1].sid)

    # Sort by weight
    context.today_pairs = [b for a, b in sorted(zip(rel_weights, context.today_pairs),
                                                key=lambda x: abs(x[0]), reverse=True)]
    rel_weights.sort(key=lambda x: -abs(x))

    trade_count = context.max_pairs - len(context.pair_pos)

    # Order pairs
    for ind, pair in enumerate(context.today_pairs[0:trade_count]):
        # if len(context.pair_pos) == context.max_pairs:
        #    return
        if rel_weights[ind] != 0:
            context.pair_hist[pair]["weight"] += abs(rel_weights[ind])
            context.pair_hist[pair]["cur_weight"] = abs(rel_weights[ind])
            if (rel_weights[ind] < 0):
                amount = -value
            else:
                amount = value
            order_pair(context, pair, amount)
            context.pair_pos.append(pair)


def order_pair(context, pair, value):
    order_value(pair[0], value)
    order_value(pair[1], -value)


def close_pair(context, data, pair):
    for security in pair:
        pos = context.portfolio.positions[security].amount
        price = data.current(security, 'price')
        init_price = context.portfolio.positions[security].cost_basis
        profit = (price - init_price) * pos
        context.pair_hist[pair]["profit"] += profit
    context.pair_hist[pair]["nTrades"] += 1
    order_target_percent(pair[0], 0)
    order_target_percent(pair[1], 0)


# Function to get all cointegrated pairs
def get_pairs(context, data):
    # print "Get Pair"
    context.stock_list.loc[:, "isInt1"] = context.stock_list["sid"].map(lambda sec: check_Int1(context, sec))
    context.stock_group = context.stock_list[context.stock_list["isInt1"].values]. \
        groupby("industry")
    context.paircount = 0
    for key, group in context.stock_group:
        group_sids = group["sid"].tolist()
        group_sids.sort(key=lambda x: x.sid)
        if len(group_sids) > 1:
            for pair in combinations(group_sids, 2):
                context.paircount += 1
                if check_coint(context, pair):
                    context.today_pairs.append(pair)
                    if pair in context.pair_hist:
                        None
                    else:
                        context.pair_hist[pair] = {}
                        context.pair_hist[pair]["stock1"] = pair[0].asset_name
                        context.pair_hist[pair]["stock2"] = pair[1].asset_name
                        context.pair_hist[pair]["profit"] = 0
                        context.pair_hist[pair]["nTrades"] = 0
                        context.pair_hist[pair]["weight"] = 0
                        context.pair_hist[pair]["cur_weight"] = 0


# Function that computes weight by possible upside
def get_weight(context, data, pair, dev_cutoff, dev_ceil=3):
    price_diff = context.price_hist[pair[0]].sub(context.price_hist[pair[1]])
    mean_diff = price_diff.mean()
    sd_diff = price_diff.std()
    price1 = data.current(pair[0], "price")
    price2 = data.current(pair[1], "price")
    cur_diff = price1 - price2
    cur_deviation = abs(cur_diff - mean_diff) / sd_diff
    mprice = max(price1, price2)
    weight = 0
    #if (dev_ceil != 3):
    #    print "Hm %s,Cm %s, sd %s,cd %s,mp %s" % (mean_diff, cur_diff, sd_diff, cur_deviation, mprice)
    # Discard high volatile stock
    if (sd_diff / mprice > .1):
        return 0
    if (cur_deviation > dev_cutoff and cur_deviation < dev_ceil):
        if (cur_diff > mean_diff):
            weight = (-1.0 * cur_deviation)
        else:
            weight = (1.0 * cur_deviation)
    return weight


# Get historical price
def hist_price(context, data):
    # print "Price History"
    if (context.first_run):
        all_stocks = context.stock_list["sid"].tolist()
        context.price_hist = data.history(all_stocks, "price", context.stationary_window, '1d')
        context.first_run = False
    else:
        hist_stocks = context.price_hist.columns.tolist()
        prev_price = data.history(hist_stocks, "price", 1, '1d')
        context.price_hist = pd.concat([context.price_hist.iloc[1:, :],
                                        prev_price])
        hist_stock_ids = [sec.sid for sec in hist_stocks]
        today_only_stocks = [sec for sec in context.stock_list["sid"] if sec.sid not in hist_stock_ids]
        today_stock_hist = data.history(today_only_stocks, "price", context.stationary_window, '1d')
        context.price_hist = pd.concat([context.price_hist,
                                        today_stock_hist], axis=1)


def check_Int1(context, sid):
    data_x = context.price_hist[sid].diff()[1:]
    if data_x.isnull().any():
        return False
    else:
        return is_stationary(data_x, context.signi_level)


def check_coint(context, pair):
    data_x = context.price_hist[pair[0]]
    data_y = context.price_hist[pair[1]]
    return is_cointegrated(context, pair, data_x, data_y, context.signi_level)


def is_stationary(data_x, cutoff):
    # Augmented Dickey-Fuller unit root test
    p_value = adfuller(data_x)[1]
    if p_value < cutoff:
        return True
    else:
        return False


def is_cointegrated(context, pair, data_x, data_y, cutoff=0.05):
    # Check linear reg
    X = statm.add_constant(data_x)
    linear_comb = statm.OLS(data_y, X)
    fitted = linear_comb.fit()
    const, beta = fitted.params
    residual = fitted.resid
    if (beta < 0):
        # print "--------- Negative Beta---------"
        return False
    else:
        # Check if linear combination is I(0)
        return is_stationary(residual, cutoff)


def pipeline_data(context):
    context.selection = make_us_equity_universe(context.population_size, rankby=valuation.market_cap.latest,
                                                mask=context.universe, max_group_weight=0.1,
                                                groupby=asset_classification.morningstar_industry_code.latest)
    industry = asset_classification.morningstar_industry_code.latest

    # Define a column dictionary that holds all the Factors
    pipe_columns = {
        'industry': industry
    }

    # Create a pipeline object with the defined columns and screen.
    pipe = Pipeline(columns=pipe_columns, screen=context.selection)
    return pipe


def my_assign_weights(context, data):
    """
    Assign weights to securities that we want to order.
    """
    pass


def track_status(context, data):
    """
    Plot variables at the end of each day.
    """
    # print(context.pair_hist.values())
    # print context.account.leverage
    # print([ a.asset_name + "  |  " + b.asset_name for a,b in context.pair_pos])
    # print "Total Pairs %s, coin pairs %s" % (context.paircount,len(context.today_pairs))
    #if get_datetime().date() == get_environment('end').date():
    #    for pair in context.pair_hist.keys():
    #        if context.pair_hist[pair]["profit"] < 0:
    #            print "%s  | %s : n=%s, pl=%s, mpl=%s, weight=%s" % (
    #            context.pair_hist[pair]['stock1'], context.pair_hist[pair]['stock2'],
    #            context.pair_hist[pair]['nTrades'], context.pair_hist[pair]['profit'],
    #            context.pair_hist[pair]['profit'] / context.pair_hist[pair]['nTrades'],
    #            context.pair_hist[pair]["weight"])

    pass
