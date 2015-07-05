-- Week 1 SQL Assignment
-- Question 1
select count(*) from flights;

--Question 2
select f.carrier,a.name, count(*) as "Total Number of Flights" from flights f,airlines a where f.carrier=a.carrier group by f.carrier,a.name;

--Question 3
select f.carrier,name,count(*) as "Number of flights" from flights f,airlines a where f.carrier=a.carrier group by f.carrier,name order by count(*) desc;

--Question 4
select f.carrier,name,count(*) as "Number of flights" from flights f,airlines a where f.carrier=a.carrier group by f.carrier,name order by count(*) desc limit 5;

--Question 5
select f.carrier,name,count(*) as "Number of flights" from flights f,airlines a where f.carrier=a.carrier and distance >= 1000 group by f.carrier,name order by count(*) desc limit 5;


--Question 6  Show the airlines with mean delay greater that 10 in descending order of mean delay
select f.carrier,name,cast(sum(dep_delay) as decimal(12,2))/count(*) as "Mean Delay" from flights f,airlines a where f.carrier=a.carrier group by f.carrier,name having cast(sum(dep_delay) as decimal(12,2))/count(*) > 10 order by 3 desc;


