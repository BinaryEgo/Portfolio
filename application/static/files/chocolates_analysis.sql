/*Uses the csv files found here: 
https://www.kaggle.com/datasets/andrewmvd/chocolate-ratings/code
*/

CREATE DATABASE IF NOT EXISTS chocolatesdb;
USE chocolatesdb;

CREATE TABLE IF NOT EXISTS chocolate_makers(
    company VARCHAR(255),
    city VARCHAR(255),
    state_or_province VARCHAR(255),
    owner_or_maker VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS chocolate_bars(
    ref INT,
    company VARCHAR(255),
    company_location VARCHAR(255),
    review_date YEAR,
    country_of_bean_origin VARCHAR(255),
    bean_origin_or_bar_name VARCHAR(255),
    cocoa_percent CHAR(4),
    ingredients VARCHAR(255),
    most_memorable_characteristics VARCHAR(255),
    rating DECIMAL(3,2)
);

/* load data from the csv files */
-- LOAD DATA LOCAL INFILE
-- "path/to/chocolate_makers.csv"
-- INTO TABLE chocolatesdb.chocolate_makers
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (company, city, state_or_province, owner_or_maker, country)
-- ;

-- LOAD DATA LOCAL INFILE
-- "path/to/chocolate_ratings.csv"
-- INTO TABLE chocolatesdb.chocolate_bars
-- FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (ref, company, company_location, review_date, country_of_bean_origin, bean_origin_or_bar_name,
-- cocoa_percent, ingredients, most_memorable_characteristics, rating)
-- ;

/*change cocoa percent string to INT*/
UPDATE chocolate_bars
SET cocoa_percent = REPLACE(cocoa_percent, "%","")
WHERE review_date IS NOT NULL
;
ALTER TABLE chocolate_bars MODIFY cocoa_percent INT;


/*add columns for further ingredient analysis*/
ALTER TABLE chocolate_bars
ADD COLUMN sugar CHAR(10),
ADD COLUMN sweetener CHAR(10), 
ADD COLUMN cocoa_butter CHAR(10), 
ADD COLUMN vanilla CHAR(10),
ADD COLUMN lecithin CHAR(10),
ADD COLUMN salt CHAR(10)
;

UPDATE chocolate_bars
SET sugar = "Y"
WHERE ingredients LIKE "%S%" 
AND ingredients NOT LIKE "%S*%" 
AND ingredients NOT LIKE "%Sa%"
;
UPDATE chocolate_bars
SET sweetener = "Y"
WHERE ingredients LIKE "%S*%"
;
UPDATE chocolate_bars
SET cocoa_butter = "Y"
WHERE ingredients LIKE "%C%"
;
UPDATE chocolate_bars
SET vanilla = "Y"
WHERE ingredients LIKE "%V%"
;
UPDATE chocolate_bars
SET lecithin = "Y"
WHERE ingredients LIKE "%L%"
;
UPDATE chocolate_bars
SET salt = "Y"
WHERE ingredients LIKE "%Sa%"
;

SELECT * FROM chocolate_makers;
SELECT * FROM chocolate_bars;

-- Where do chocolates reviewed come from?
SELECT
	city,
    state_or_province,
    country,
    COUNT(chocolate_bars.bean_origin_or_bar_name) AS total
FROM chocolate_bars
JOIN chocolate_makers ON chocolate_bars.company = chocolate_makers.company
GROUP BY city
ORDER BY total DESC
;

-- How many chocolates were reviewed per year?
SELECT
	review_date AS 'year',
    COUNT(bean_origin_or_bar_name) AS total
FROM chocolate_bars
GROUP BY review_date HAVING total > 0
ORDER BY review_date
;

-- According to Brelinski, which manufacturers make the best craft chocolates? --
SELECT
	chocolate_makers.company,
    owner_or_maker,
	country,
    MIN(rating) AS min_rating,
    AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_makers
JOIN chocolate_bars ON chocolate_makers.company = chocolate_bars.company
GROUP BY chocolate_makers.company
ORDER BY avg_rating DESC
LIMIT 5
;

-- Which make the worst? --
SELECT
	chocolate_makers.company,
    owner_or_maker,
	country,
    MIN(rating) AS min_rating,
    AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_makers
JOIN chocolate_bars ON chocolate_makers.company = chocolate_bars.company
GROUP BY chocolate_makers.company
ORDER BY avg_rating ASC
LIMIT 5
;

-- Where do the best chocolate bars get their beans from? --
SELECT
    country_of_bean_origin,
    AVG(rating) AS avg_rating
FROM chocolate_bars
GROUP BY country_of_bean_origin
ORDER BY avg_rating DESC
LIMIT 5
;

-- Is there a relationship between cocoa percent and Brelinski's rating?
SELECT
    cocoa_percent,
	AVG(rating)
FROM chocolate_bars
WHERE cocoa_percent IS NOT NULL
GROUP BY cocoa_percent
ORDER BY cocoa_percent
;

-- What combination of ingredients produce the best tasting chocolate? --
SELECT
	ingredients, 
    AVG(rating) AS avg_rating
FROM chocolate_bars
GROUP BY ingredients
ORDER BY avg_rating DESC
LIMIT 1
;

-- Other than cocoa beans, which ingredient is most vital to a good rating? --
SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY sugar HAVING sugar="Y" 
; 
/*sugar = 1 , 3.219497 , 4*/

SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY sweetener HAVING sweetener="Y" 
;
/*sweetener = 1.5 , 2.996711 , max = 3.75*/

SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY cocoa_butter HAVING cocoa_butter="Y" 
; 
/*cocoa_butter= 1 , 3.211481 , 4*/

SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY vanilla HAVING vanilla="Y" 
; 
/*vanilla = 1 , 3.150609 , 4*/

SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY lecithin HAVING lecithin="Y" 
; 
/*lecithin = 1 , 3.033286 , 4*/

SELECT
	MIN(rating) AS min_rating,
	AVG(rating) AS avg_rating,
    MAX(rating) AS max_rating
FROM chocolate_bars
GROUP BY salt HAVING salt="Y" 
; 
/*1.5, 3.027027, 3.75*/


