-- I used two methods to study how weather conditions are associated with New York Delays
--     First I looked at correlation between the conditions and delay to look at 
--		overall impact of the condition on delay
--     Then I checked the mean delay for a range of condition value for each weather condition 
--		to see if extreme conditions affect delay

-- Question 1
-- Check Correlation 
-- One way to check the effect of weather condition is look at the correlation between the weather condition and delay
-- Based on the observation of the correlation it appears that Temp, Dew, Pressure and Visibility affects the delay
SELECT
  corr(temp,dep_delay) "Temp_Effect",
  corr(dewp,dep_delay) "Dew_Effect",
  corr(humid,dep_delay)"Humid_Effect",
  corr(wind_dir,dep_delay) "WindDir_Effect",    
  corr(wind_speed,dep_delay) "WindSpeed_Effect",
  corr(wind_gust,dep_delay) "WindGust_Effect", 
  corr(pressure,dep_delay) "Pressure_Effect", 
  corr(precip,dep_delay) "Precip_Effect",  
  corr(visib,dep_delay) "Visibility_Effect"
FROM
  (SELECT 
	  f.*,
	  w.temp,
	  w.dewp,
	  w.humid,
	  w.wind_dir,    
	  w.wind_speed,	
	  w.wind_gust, 
	  w.pressure, 
	  w.precip,  
	  w.visib
  FROM 
     weather w, 
     flights f 
  WHERE 
     f.origin in ('JFK','LGA') AND 
     w.year = f.year AND
     w.month = f.month AND
     w.day = f.day AND
     ((w.hour = f.hour AND f.minute <= 30) OR
     (w.hour + 1  = f.hour AND f.minute > 30))) AS "NewYork_Delays";


-- Question 1, Second Step
-- Checked the mean delay for a range of condition value for each weather condition 
--		to see if extreme conditions affect delay

-- I created a table to combine the weather condition at departure time with new york flights
-- Then I ran individual query to check average delay for given range of weather condition value.

-- My observation for each weather condition is given as comment just before the query that provides 
-- 	average delay for multiple range of that weather condition value

-- Create a table which has all new york flights and the weather condition during time of departure
CREATE TABLE newyork_delays_depCond
AS
SELECT 
  f.*,
  w.temp,
  w.dewp,
  w.humid,
  w.wind_dir,    
  w.wind_speed,
  w.wind_gust, 
  w.pressure, 
  w.precip,  
  w.visib
FROM 
  weather w, 
  flights f 
WHERE 
  f.origin in ('JFK','LGA') AND 
  w.year = f.year AND
  w.month = f.month AND
  w.day = f.day AND
  ((w.hour = f.hour AND f.minute <= 30) OR
   (w.hour + 1  = f.hour AND f.minute > 30));

-- High temperature is associated with high delay
-- Check average delay for a range of temparture values.. In order to obtain the range I followed simple method of 
-- 	dividing the temparature by 10 and rounding of (which implies range of 10F). I applied similar method for 
--      weather conditions as well
SELECT
  round(temp/10) AS "Temp_Range", 
  avg(dep_delay) As "Mean_Delay", 
  count(*)
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Very high Dew point causes delay
SELECT
  round(dewp/10) AS "Dew_Range", 
  avg(dep_delay) As "Mean_Delay", 
  count(*)
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Humidity seems to have not much effect on delays
SELECT
  round(humid/10) AS "Humid_Range", 
  avg(dep_delay) As "Mean_Delay",
  count(*) 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Particular wind direction (96 to 120) seems to have any effect on delay. 
SELECT
  round(wind_dir/12) AS "Wind_Direction", 
  avg(dep_delay) As "Mean_Delay",
  count(*) 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Wind speed above 35 mph seems to increase the delays
SELECT
  round(wind_speed/5) AS "Wind_Speed_Range", 
  avg(dep_delay) As "Mean_Delay",
  count(*) 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Wind speed gust above 35 mph seems to increase the delays
SELECT
  round(wind_gust/5) AS "Wind_gust_Range", 
  avg(dep_delay) As "Mean_Delay",
  count(*) 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Percipitation doesn't seems to impact delay
SELECT
  round(precip/.05) AS "Percip_Range", 
  avg(dep_delay) As "Mean_Delay",
  count(*)
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Delays are less when pressure is high
SELECT
  round(pressure/5) AS "Pressure_Range", 
  avg(dep_delay) As "Mean_Delay",
  count(*) 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Low visibility has moderate impact on delay
SELECT
  round(visib/.5) AS "Visibility_Range", 
  avg(dep_delay) As "Mean_Delay" 
FROM newyork_delays_depCond
GROUP BY 1
ORDER BY 1;

-- Question 2
-- Check Correlation
-- Based on correlation it appears the age of flight doesn't affect delay
SELECT
  corr(f.year-p.year,dep_delay) "Age Effect"
FROM
  flights f,
  planes p
WHERE
  f.tailnum = p.tailnum;

-- Question 2, second step
-- Let's check the mean delay by age to see if any particular age (say very old) has any impact on delay
--             Based on the results of following query it appears age doesn't have any effect on delay
SELECT
  f.year-p.year AS "Age",
  avg(f.dep_delay) As "Mean_Delay",
  count(*)
FROM
  flights f,
  planes p
WHERE
  f.tailnum = p.tailnum
GROUP BY 1
ORDER BY 1;

-- Question 3 (My own Question)
-- Planes from whcih manufacturer have minimum average delay? The manufacturer's plan must have atleast 1000 flights
-- "MCDONNELL DOUGLAS" has minimum average delay 
SELECT
  manufacturer,
  avg(f.dep_delay) As "Mean_Delay",
  count(*)
FROM
  flights f,
  planes p
WHERE
  f.tailnum = p.tailnum
GROUP BY 1 
HAVING
   count(*) >= 1000
ORDER BY 2
LIMIT 1;
