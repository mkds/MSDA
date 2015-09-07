#Question 1
SELECT 
    COUNT(*) 'Planes with Listed Speed',
    MIN(speed) 'Minimum Speed',
    MAX(speed) 'Maaximum Speed'
FROM
    planes
WHERE
    speed IS NOT NULL
    
;

#Question 2 - Part 1 Total Distance
SELECT 
    SUM(distance)
FROM
    flights
WHERE
    year = 2013 AND month = 1;

#Question 2 - Part 2 Total Distance when tailnum is missing
SELECT 
    SUM(distance)
FROM
    flights
WHERE
    year = 2013 AND month = 1
        AND tailnum IS NULL;
        
#Question 3 - Part 1 Inner Join
SELECT 
    manufacturer, SUM(distance)
FROM
    flights,
    planes
WHERE
    flights.year = 2013 AND month = 7
        AND day = 5
        AND flights.tailnum = planes.tailnum
GROUP BY planes.manufacturer;


#Question 3 - Part 2 Outer join
# Results on left outer join inclues all the values from left table (i.e. flights) table even when there is no matching value on right table for the column used in the join
SELECT 
    manufacturer, SUM(distance)
FROM
    flights
        LEFT JOIN
    planes ON flights.tailnum = planes.tailnum
WHERE
    flights.year = 2013 AND month = 7
        AND day = 5
GROUP BY planes.manufacturer;

#Question 4 List the number of flights by airline and Destination on 1/1/2013
SELECT 
    airlines.name 'Airline',
    airports.name 'Destination',
    COUNT(*) 'Number of Flights'
FROM
    airlines,
    flights,
    airports
WHERE
    flights.year = 2013
        AND flights.month = 1
        AND day = 1
        AND flights.carrier = airlines.carrier
        AND flights.dest = airports.faa
GROUP BY airlines.name , airports.name
ORDER BY 1 , 2;