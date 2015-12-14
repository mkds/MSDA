
#Column width of variables
sel_widths = c(16,1 ,1 ,10,4 ,6,18,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,4,1 ,1 ,1 ,1 ,1 ,1 ,2 ,1 ,1 ,1 ,8 ,1 ,7 ,1 ,4 ,1 ,1 ,1 ,2,1 ,1,1 ,1 ,1 ,1 ,1 ,3 ,1 ,1 ,1 ,1 ,2 ,1,273,5)
#Name of the variables.
var_names = c("ignore","age","sex","ignore0","height","Weight","ignore1","felt_depressed","consider_suicide","plan_suicide","attempt_suicide","ignore2","ever_smoke","age_first_smoke","smoked_past30days","smoke_per_day","ignore3","chewing","ignore4","days_alcohol","first_drink_alcohol","alcohol_past30days","two_hour_drinks","ignore5","times_marijuana","first_marijuana","marijuana_past30days","ignore6","offered","ignore7","self_describe_weight","ignore8","drink_juice","eat_fruit","eat_green_salad","ignore8","eat_vegetables","ignore9","drink_milk","eat_breakfast","physical_activity","tv_hours","video_games_hours","ignore10","diagnosed_asthma","ignore11","exercise_past7days","tested_hiv","ignore12","avg_sleep","ignore13","BMIPCT")
file_loc = "https://raw.githubusercontent.com/mkds/MSDA/master/IS607/Project/data/yrbs2013.dat"
yb = read.fwf(file_loc,widths = sel_widths, col.names=var_names,stringsAsFactors=F)
dim(yb)

#Only keep the the columns that we are intrested in
yb = yb[-grep("ignore",var_names)]
str(yb)

yb$felt_depressed = factor(yb$felt_depressed,levels=c(1,2),labels=c("depressed","not-depressed"))
yb$plan_suicide = factor(yb$plan_suicide,levels=c(1,2),labels=c("planned_suicide","No-suicide_plan"))
yb$diagnosed_asthma = factor(yb$diagnosed_asthma,levels=c(1,2),labels=c("diagnosed_asthma","Not-diagnosed_asthma"))
yb$ever_smoke = factor(yb$ever_smoke,levels=c(1,2),labels=c("Smoked","Never_Smoked"))
yb$self_describe_weight = factor(yb$self_describe_weight,levels=c(1,2,3,4,5),labels=c("Very UnderWeight","Slightly Underwight","Right weight","Slightly Overweight","Very overweight"))
yb$tested_hiv = factor(yb$tested_hiv,levels=c(1,2,3),labels=c("tested_HIV","Not-tested_HIV","Not sure of HIV"))

yb$BMIPCT = as.double(yb$BMIPCT)
summary(yb)

yb = yb[complete.cases(yb),]

yb$smoked_past30days = yb$smoked_past30days - 1
yb$attempt_suicide = yb$attempt_suicide - 1
yb$smoke_per_day = yb$smoke_per_day - 1
yb$chewing = yb$chewing - 1
yb$days_alcohol = yb$days_alcohol - 1
yb$alcohol_past30days = yb$alcohol_past30days - 1
yb$two_hour_drinks = yb$two_hour_drinks - 1
yb$times_marijuana = yb$times_marijuana - 1
yb$marijuana_past30days = yb$marijuana_past30days - 1
yb$offered = yb$offered - 1
yb$drink_juice = yb$drink_juice - 1
yb$eat_fruit = yb$eat_fruit - 1
yb$eat_green_salad = yb$eat_green_salad - 1
yb$eat_vegetables = yb$eat_vegetables - 1
yb$drink_milk = yb$drink_milk - 1
yb$eat_breakfast = yb$eat_breakfast - 1
yb$physical_activity = yb$physical_activity - 1
yb$tv_hours = yb$tv_hours - 1
yb$video_games_hours = yb$video_games_hours - 1
yb$exercise_past7days = yb$exercise_past7days - 1

library(ggplot2)
title_theme = theme(plot.title = element_text(face = "bold",vjust = 2,size = 16))
 
ggplot(data=yb,aes(x=consider_suicide))+
  geom_bar(aes(y=..density..),fill=c("red","darkgreen"),binwidth=1,origin=-.5) +
  scale_x_discrete(breaks=c(1,2), labels=c("Suicidal Thought","No Suicidal"), limits=c(1,2)) +
  ylab("Considered Suicide") +
  xlab("Smoke/Day") +
  ggtitle("Smoking and Suicidal thought") + facet_wrap(~smoke_per_day) + 
  title_theme

ggplot(data=yb,aes(x=consider_suicide)) +
  geom_bar(aes(y=..density..),fill=c("gray","red","darkgreen"),binwidth=1,origin=-.5) +
  ylab("Considered Suicide") +
  xlab("Days_Alcohol")+
  ggtitle("Alcohol and Suicidal thought") + facet_wrap(~days_alcohol) +
  title_theme

ggplot(data=yb,aes(y=BMIPCT)) +
  geom_boxplot(aes(x=smoke_per_day,fill=as.factor(smoke_per_day))) +
  ylab("BMI Percentile") +
  xlab("Smoke/Day")  +
  scale_fill_discrete(name="Smokes/Day") +
  ggtitle("Smoking and BMI") 

ggplot(data = yb,aes(y = BMIPCT)) +
  geom_boxplot(aes(x = smoke_per_day > 2,fill = as.factor(smoke_per_day > 2))) +
  ylab("BMI Percentile") +
  xlab("More than one cigarette/Day") +
  scale_fill_discrete(name="More than Two Smokes?") +
  ggtitle("Smoking and BMI") +
  title_theme

ggplot(data = yb,aes(y = BMIPCT)) +
  geom_boxplot(aes(x = eat_breakfast,fill = as.factor(eat_breakfast))) +
  ylab("BMI Percentile") +
  xlab("Days Alcohol") +
  scale_fill_discrete(name="Breakfast/Week") +
  ggtitle("Breakfast and BMI") + 
  title_theme

ggplot(data = yb,aes(y = BMIPCT)) +
  geom_boxplot(aes(x = eat_breakfast > 4,fill = as.factor(eat_breakfast > 4))) +
  ylab("BMI Percentile") +
  xlab("Days Alcohol") +
  scale_fill_discrete(name="Regular Breakfast?") +
  ggtitle("Breakfast and BMI") + 
  title_theme

yb$BMI_Weight = factor("Normal",levels = c("Normal","Overweight","Obese"))
yb$BMI_Weight[yb$BMIPCT > 85 & yb$BMIPCT < 95] = "Overweight"
yb$BMI_Weight[yb$BMIPCT >= 95] = "Obese"

ggplot(data=yb,aes(x=as.numeric(BMI_Weight)))+
  geom_bar(aes(y=..density..),binwidth=1,origin=-.5,fill=c("gray","darkgreen","blue","red")) +
  scale_x_discrete(name="weight", breaks=c(1,2,3), labels=c("Normal","Overweight","Obese"), limits=c(1,2,3)) +
  ylab("BMI") +
  xlab("Smoke/Weight")+
  ggtitle("Smoking and Weight") + 
  facet_wrap(~smoke_per_day) +
  title_theme

ggplot(data=yb,aes(x=as.numeric(BMI_Weight)))+
  geom_bar(aes(y=..density..),binwidth=1,origin=-.5,fill=c("gray","darkgreen","blue","red")) +
  scale_x_discrete(name="weight", breaks=c(1,2,3), labels=c("Normal","Overweight","Obese"), limits=c(1,2,3)) +
  ylab("BMI") +
  xlab("Smoke/Weight")+
  ggtitle("Smoking and Weight") + 
  facet_wrap(~ever_smoke) +
  title_theme

yb_summary = NULL
yb_summary$BMIPCT = yb$BMIPCT
yb_summary$good_eat = yb$eat_fruit + yb$eat_green_salad + yb$eat_breakfast + yb$eat_vegetables + yb$drink_milk + yb$drink_juice
yb_summary$bad_eat = yb$smoke_per_day + yb$days_alcohol + yb$alcohol_past30days + yb$chewing + yb$times_marijuana
yb_summary$physical_good = yb$physical_activity + yb$exercise_past7days + yb$avg_sleep
yb_summary$physical_bad = yb$tv_hours + yb$video_games_hours  
yb_summary = as.data.frame(yb_summary)

summary(yb_summary)

#Compare the groups with bad food habbits with one with no bad habbits
t.test(yb_summary$BMIPCT[yb_summary$bad_eat>0],yb_summary$BMIPCT[yb_summary$bad_eat==0])


t.test(yb_summary$BMIPCT[yb_summary$good_eat<13],yb_summary$BMIPCT[yb_summary$good_eat>=13])

t.test(yb_summary$BMIPCT[yb_summary$good_eat<13 & yb_summary$bad_eat==0],yb_summary$BMIPCT[yb_summary$good_eat>=13 & yb_summary$bad_eat==0])

t.test(yb_summary$BMIPCT[yb_summary$physical_good<11],yb_summary$BMIPCT[yb_summary$physical_good>=11])

t.test(yb_summary$BMIPCT[yb_summary$physical_good<11  & yb_summary$bad_eat==0],yb_summary$BMIPCT[yb_summary$physical_good>=11  & yb_summary$bad_eat==0])

t.test(yb_summary$BMIPCT[yb_summary$physical_bad<6],yb_summary$BMIPCT[yb_summary$physical_bad>=6])

bmipct_model = lm(BMIPCT~.,data = yb_summary)
summary(bmipct_model)
