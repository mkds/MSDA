
## ------------------------------------------------------------------------
#Read Data
suppressMessages(library(data.table))
#Read File
news <- fread("OnlineNewsPopularity.csv", stringsAsFactors=F)
dim(news)
#Extract publication date from URL
news[,pub_date:= as.Date(gsub(".*mashable.com/(.*/.*/).*","\\1",url))]

## ------------------------------------------------------------------------
#Question 1
#Unique URL
print("Count of Unique URL")
length(unique(news$url))
#As there is no duplicates URL all the records are unique 
#Find the largest lag between publication and data collection 
print("Maximum time lag(in days) between publication and data collection")
max(news$timedelta)
#Time Frame of publication
print("Time frame of publication")
summary(news$pub_date)

## ------------------------------------------------------------------------
#Question 2
#Histogram of timedelta
hist(news$timedelta,breaks = 73,
     main="Number of Days between publication and data collection",
     xlab="Number of Days", col="orchid")
suppressMessages(library(ggplot2))

#Timedelta by month
ggplot(news) + 
  geom_point(aes(as.factor(format(pub_date,"%m")),timedelta),color="orchid") + 
  facet_grid(.~format(pub_date,"%Y")) + 
  labs(x="Month",y="Number of Days",
       title="Number of Days between publication and data collection")

## ------------------------------------------------------------------------
#Question 3
#Extract topic from URL
topics <- gsub(".*/(.*)/$","\\1",news$url)
#Get topic Frequency
topics_freq <- as.data.frame(table(topics))
#Topics are unique, hence maximum frequency is 1
top20 <- topics_freq[order(topics_freq$Freq,decreasing = T)[1:20],]
cat("\nTopic Frequency")
print(top20,row.names=F) #Topics are unique, hence maximum frequency is 1

# **Try topic frequency by first word and last word**
# Get firstword
topic_firstword <- gsub("-.*","",topics)
# Get lastword
topic_lastword <- gsub(".*-","",topics)
#Frequency by first word
firstword_freq <- as.data.frame(table(topic_firstword))
#Frequency by last word
lastword_freq <- as.data.frame(table(topic_lastword))
#Get top 25 
top25_firstword <- firstword_freq[order(firstword_freq$Freq,
                                        decreasing = T)[1:25],]
top25_lastword <- lastword_freq[order(lastword_freq$Freq,
                                      decreasing = T)[1:25],]
cat("\nTop 25 First word of topic")
print(top25_firstword,row.names = F)
cat("\nTop 25 Last word of topic")
print(top25_lastword,row.names = F )


## ------------------------------------------------------------------------
#Question 4
subtopics <- c("elon-musk","facebook","ebola","ipad","iphone",
               "tornado","sharknado","taylor-swift")
for (s in subtopics){
  #Add a column using subtopic name and set its initial value to False
  news[,s:=F,with=F]
  #Find URLs that has the subtopic as substring
  sub_present <- grep(s,news$url)
  #Set the subtopic column to true if it is substring of url
  news[sub_present,s:=T,with=F]
}
#Count by subtopics
print("Count by sub-topics(sub-string in URL)")
print(news[,lapply(.SD,sum),.SDcols=subtopics],row.names=F)

## ------------------------------------------------------------------------
#Question 5
#Count of subtopics by month
sum_by_subtop_month <- news[,lapply(.SD,sum),
                            .SDcols=subtopics,
                            by=(Year_Month=format(pub_date,"%Y-%m"))]
print("Count of sub-topic by Month")
print(sum_by_subtop_month,row.names=F)

## ------------------------------------------------------------------------
#Question 6
cols_to_analyze <- c("shares","num_videos","num_imgs",
                     "abs_title_subjectivity","abs_title_sentiment_polarity")
print("Mean values Weekend Vs Non-Weekend")
print(news[,lapply(.SD,mean),.SDcols=cols_to_analyze,by=is_weekend],
      row.names = F)

## ------------------------------------------------------------------------
#Question 7
#Number of Shares Weekend Vs non-weekend for Entertainment News
entertain_shares <- news[data_channel_is_entertainment > 0,lapply(.SD,mean),
                        .SDcols=cols_to_analyze,
                        by=is_weekend]
#Number of Shares Weekend Vs non-weekend for lifestyle News
lifestyle_shares <- news[data_channel_is_lifestyle > 0,lapply(.SD,mean),
                         .SDcols=cols_to_analyze,
                         by=is_weekend]
#Number of Shares Weekend Vs non-weekend for Tech News
tech_shares <- news[data_channel_is_tech > 0,lapply(.SD,mean),
                    .SDcols=cols_to_analyze,
                    by=is_weekend]
#Number of Shares Weekend Vs non-weekend for World News
world_shares <- news[data_channel_is_world > 0,
                     lapply(.SD,mean),
                     .SDcols=cols_to_analyze,by=is_weekend]
print("Mean values Weekend Vs Non-Weekend for Entertainment News")
print(entertain_shares, row.names=F)
print("Mean values Weekend Vs Non-Weekend for lifestyle News")
print(lifestyle_shares,row.names = F)
print("Mean values Weekend Vs Non-Weekend for Tech News")
print(tech_shares, row.names = F)
print("Mean values Weekend Vs Non-Weekend for World News")
print(world_shares, row.names = F)
## ------------------------------------------------------------------------

