--### From the two most commonly appearing regions, which is the latest datasource?

SELECT DISTINCT datasource
FROM trips
JOIN datasource USING (id)
WHERE (region,
       datetime) in
    (SELECT t.region,
            max(t.datetime)
     FROM trips t,
       (SELECT region,
               sum(qty) qty
        FROM trips
        GROUP BY region
        ORDER BY region DESC
        LIMIT 2) m
     WHERE t.region=m.region
     GROUP BY t.region);
	 
--### 	 What regions has the "cheap_mobile" datasource appeared in?

SELECT DISTINCT region
FROM trips
JOIN datasource USING (id)
WHERE datasource='cheap_mobile';