/*
	Create schema
*/
IF SCHEMA_ID('web') IS NULL BEGIN	
	EXECUTE('CREATE SCHEMA [web]');
END
GO

/*
	Create user to be used in the sample API solution
*/
IF USER_ID('PythonWebApp') IS NULL BEGIN	
	CREATE USER [PythonWebApp] WITH PASSWORD = 'a987REALLY#$%TRONGpa44w0rd';	
END

/*
	Grant execute permission to created users
*/
GRANT EXECUTE ON SCHEMA::[web] TO [PythonWebApp];
GO

/*
	Return details on a specific customer
*/
CREATE OR ALTER PROCEDURE web.get_customer
@Json NVARCHAR(MAX)
AS
SET NOCOUNT ON;
DECLARE @CustomerId INT = JSON_VALUE(@Json, '$.CustomerID');
SELECT 
	[CustomerID], 
	[FirstName], 
	[EmailAddress]
FROM 
	[SalesLT].[Customer] 
WHERE 
	[CustomerID] = @CustomerId
FOR JSON PATH
GO

/*
	Delete a specific customer
*/
CREATE OR ALTER PROCEDURE web.delete_customer
@Json NVARCHAR(MAX)
AS
SET NOCOUNT ON;
DECLARE @CustomerId INT = JSON_VALUE(@Json, '$.CustomerID');
DELETE FROM [SalesLT].[Customer] WHERE CustomerId = @CustomerId;
SELECT * FROM (SELECT CustomerID = @CustomerId) D FOR JSON AUTO;
GO

/*
	Update (Patch) a specific customer
*/
CREATE OR ALTER PROCEDURE web.patch_customer
@Json NVARCHAR(MAX)
AS
SET NOCOUNT ON;
DECLARE @CustomerId INT = JSON_VALUE(@Json, '$.CustomerID');
WITH [source] AS 
(
	SELECT * FROM OPENJSON(@Json) WITH (
		[CustomerID] INT, 
		[FirstName] NVARCHAR(100), 
		[EmailAddress] NVARCHAR(100)
	)
)
UPDATE
	t
SET
	t.[FirstName] = COALESCE(s.[FirstName], t.[FirstName]),
	t.[EmailAddress] = COALESCE(s.[EmailAddress], t.[EmailAddress])
FROM
	[SalesLT].[Customer] t
INNER JOIN
	[source] s ON t.[CustomerID] = s.[CustomerID]
WHERE
	t.CustomerId = @CustomerId;

DECLARE @Json2 NVARCHAR(MAX) = N'{"CustomerID": ' + CAST(@CustomerId AS NVARCHAR(9)) + N'}'
EXEC web.get_customer @Json2;
GO

/*
	Create a new customer
*/

CREATE OR ALTER PROCEDURE web.put_customer
@Json NVARCHAR(MAX)
AS
SET NOCOUNT ON;
DECLARE @CustomerId INT = NEXT VALUE FOR Sequences.CustomerID;
WITH [source] AS 
(
	SELECT * FROM OPENJSON(@Json) WITH (		
			[FirstName] NVARCHAR(100), 
		[EmailAddress] NVARCHAR(100)
	)
)
INSERT INTO [SalesLT].[Customer] 
(
	CustomerID, 
	FirstName, 	
	EmailAddress
	)
SELECT
	@CustomerId, 
	FirstName, 
	EmailAddress
FROM
	[source]
;

DECLARE @Json2 NVARCHAR(MAX) = N'{"CustomerID": ' + CAST(@CustomerId AS NVARCHAR(9)) + N'}'
EXEC web.get_customer @Json2;
GO

CREATE OR ALTER PROCEDURE web.get_customers
AS
SET NOCOUNT ON;
-- Cast is needed to corretly inform pyodbc of output type is NVARCHAR(MAX)
-- Needed if generated json is bigger then 4000 bytes and thus pyodbc trucates it
-- https://stackoverflow.com/questions/49469301/pyodbc-truncates-the-response-of-a-sql-server-for-json-query
SELECT CAST((
	SELECT 
		[CustomerID], 
		[CustomerName]
	FROM 
		[Sales].[Customers] 
	FOR JSON PATH) AS NVARCHAR(MAX)) AS JsonResult
GO

