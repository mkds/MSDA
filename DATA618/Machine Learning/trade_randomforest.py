from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline, CustomFactor
from quantopian.pipeline.filters import StaticAssets, Q500US, make_us_equity_universe, Q1500US
from sklearn.ensemble import RandomForestClassifier
from quantopian.pipeline.data.quandl import cboe_vix
from collections import deque
from quantopian.pipeline.data.psychsignal import stocktwits_free


def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # Provide list of stocks to be considered for trading
    context.security = [sid(17080),sid(1091),sid(4151),sid(3149)]
    context.train_period = 170
    context.return_period = 5
    context.features = {}
    context.cur_features = {}
    context.outcome = {}
    context.price_window = 20
    context.pred = deque(maxlen=context.return_period + 1)
    context.nrun = 0
    context.hist_sentiment = {}
    for st in context.security:
        context.hist_sentiment[st]=deque(maxlen=context.train_period + context.return_period)
    context.score = 0
    # Pattern Trading
    schedule_function(pattern_trading, date_rules.every_day(), time_rules.market_open(hours=1))


    # Pipeline for sentiment data
    attach_pipeline(pipeline_data(context), 'aux_data')



def pattern_trading(context, data):
    """
    Trade based on the prediction made by random forest model
    """
    #Get sentiment data
    pout = pipeline_output('aux_data')
    #print(pout)
    #Accumulate sentiment data
    for st in context.security:
        context.hist_sentiment[st].append(pout['sentiment'][st])

    #If enough data is available then train the model
    if context.nrun == (context.train_period + context.return_period):
        # hist_price(context,data)
        print(context.nrun)
        get_train_features(context, data)
        train_model(context, data)
    #Once model is trained, get predictions
    elif context.nrun > (context.train_period + context.return_period):
        #Re-train with recent data every 20 days
        if context.nrun % 20 == 0:
            get_train_features(context, data)
            train_model(context, data)
        #Get prediction and trade
        if context.nrun % context.return_period == 0:
            get_predict_features(context, data)
            predict_outcome(context, data)
            order_stock(context, context.selected_stock)
    context.nrun += 1


def order_stock(context, stock):
    #If we switched the trading stock then sell the previous stock
    if len(context.portfolio.positions) > 0 and context.portfolio.positions.keys()[0] != stock:
        order_target_percent(context.portfolio.positions.keys()[0],0)
     #Trade short or long based on the prediction
    if (context.pred[0] == 'Pos'):
        order_target_percent(stock, 1)
    elif (context.pred[0] == 'Neg'):
        order_target_percent(stock, -1)



def pipeline_data(context):
    #Sentiment data
    pipe_columns = {
        'sentiment': stocktwits_free.bullish_intensity.latest
    }

    pipe = Pipeline(columns=pipe_columns, screen=StaticAssets(context.security))
    return pipe

def get_train_features(context, data):
    #Get features for training
    all_stocks = context.security
    context.price_hist = data.history(all_stocks, "price", context.train_period + context.return_period, '1d')
    #Collect features for each stock
    for st in context.security:
        #Features
        context.features[st] = []
        #Outcome variable
        context.outcome[st] = []

        prices = context.price_hist[st][:-1]

        for i in range(context.train_period - context.price_window - 1):
            #Price features
            prev_prices = prices[i:(i + context.price_window)]
            features = prev_prices.diff()[1:].tolist()
            sma_diff = prev_prices.mean() - prev_prices[-1]
            features.append(sma_diff)
            #Sentiment feature
            features += list(context.hist_sentiment[st])[i:(i + context.price_window)]
            context.features[st].append(features)
            #Outcome variable based on return
            outcome = "Neu"
            if (prices[(i + context.price_window + context.return_period - 1)] / prices[
                (i + context.price_window - 1)]) > 1.005:
                outcome = "Pos"
            if (prices[(i + context.price_window + context.return_period - 1)] / prices[
                (i + context.price_window - 1)]) < 0.995:
                outcome = "Neg"

            context.outcome[st].append(outcome)



def train_model(context, data):
    classifier = RandomForestClassifier(max_depth=3, random_state=100, n_estimators=15)
    context.score = 0
    #Train one model for each stock and select best model based on the test set performance
    for st in context.security:
        print len(context.features[st])
        n = len(context.features[st])
        #Use 80% for training and 20% of testing
        train_features = context.features[st][:int(n * .8)]
        train_outcome = context.outcome[st][:int(n * .8)]
        test_features = context.features[st][int(n * .8):]
        test_outcome = context.outcome[st][int(n * .8):]
        print(len(test_outcome))
        print(len(train_outcome))
        model = classifier.fit(train_features,
                                       train_outcome)
        score = model.score(test_features, test_outcome)
        if score > context.score:
            context.score = score
            #Train the best model on all data
            context.model = classifier.fit(context.features[st],
                                       context.outcome[st])
            context.selected_stock = st
    #print("****** Selected: ",context.selected_stock.asset_name," Score",context.score)


def get_predict_features(context, data):
    """
    Prepare features for prediction
    """
    all_stocks = context.selected_stock
    price_hist = data.history(all_stocks, "price", context.price_window + 1, '1d')
    features = price_hist[:-1].diff()[1:].tolist()
    sma_diff = price_hist.mean() - price_hist[-2]
    features.append(sma_diff)
    features += (list(context.hist_sentiment[context.selected_stock])[-context.price_window:])
    context.cur_features[context.selected_stock] = features



def predict_outcome(context, data):
    # Predict outcome
    context.pred.append(context.model.predict(context.cur_features[context.selected_stock]))
