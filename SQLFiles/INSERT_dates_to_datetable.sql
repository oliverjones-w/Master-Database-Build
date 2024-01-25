


DECLARE @StartDate DATETIME = '1950-01-01',
    @EndDate DATETIME = '2100-01-01';

--- Recursive CTE to generate dates
;WITH DateRange(Date) AS (
    SELECT @StartDate AS DATE
    UNION ALL
    SELECT DATEADD(DAY, 1, Date)
    FROM DateRange
    WHERE Date < @EndDate
)

-- Inserting data into the Date table
INSERT INTO Date (Date, Year, Quarter, Month, Week, DayofWeek)
SELECT
    Date, 
    YEAR(Date) AS Year,
    DATEPART(QUARTER, Date) AS QUARTER,
    MONTH(Date) AS Month,
    DATEPART(WEEK, Date) AS Week,
    DATEPART(WEEKDAY, Date) AS DayofWeek
FROM
    DateRange
OPTION (MAXRECURSION 0);