USE EGX_Data;

-- DROP TABLE Staging_Financials

SELECT * FROM Staging_Financials


CREATE OR ALTER VIEW Fact_Financials AS 
SELECT 
    Line_Order,
    Company,
    Statement,
    Line_Item,
    EOMONTH(
        DATEFROMPARTS(
            TRY_CAST(RIGHT(Period, 4) AS INT),
            TRY_CAST(SUBSTRING(Period, 2, 1) AS INT) * 3,
            1
        )
    ) AS EndOfQuarter,
    Amount
FROM Staging_Financials;


SELECT * FROM Fact_Financials ORDER BY Line_Order


CREATE VIEW DimAccount AS
WITH FinanceIndex AS (
    SELECT DISTINCT
        Statement,
        Line_Item
    FROM Fact_Financials
)
SELECT
    ROW_NUMBER() OVER (
        ORDER BY Statement, Line_Item
    ) AS FinanceIndex,
    Statement,
    Line_Item
FROM FinanceIndex;

SELECT * FROM DimAccount


CREATE VIEW DimCompany AS
SELECT DISTINCT
    Company
FROM Fact_Financials;

SELECT * FROM DimCompany


CREATE VIEW DimStatement AS
SELECT DISTINCT
    CASE
        WHEN Statement = 'income-statement' THEN 'Income_Statement'
        WHEN Statement = 'balance-sheet' THEN 'Balance_Sheet'
        WHEN Statement = 'cash-flow-statement' THEN 'Cash_Flow'
    END AS Statement_Type
FROM Fact_Financials;

SELECT * FROM DimStatement


CREATE VIEW DimCalendar AS
SELECT DISTINCT
    EndOfQuarter,
    YEAR(EndOfQuarter) AS Year,
    DATEPART(QUARTER, EndOfQuarter) AS Quarter,
    CONCAT(YEAR(EndOfQuarter), '_', DATEPART(QUARTER, EndOfQuarter)) AS Quarter_Year
FROM Fact_Financials;

SELECT * FROM DimCalendar