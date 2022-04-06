USE retail;
GO

DROP TRIGGER IF EXISTS IfStoreTypeExists
GO
CREATE TRIGGER IfStoreTypeExists ON StoreTypes
INSTEAD OF INSERT
AS
BEGIN
	INSERT INTO StoreTypes
	SELECT * FROM inserted
	WHERE storetype_id NOT IN (SELECT storetype_id FROM StoreTypes)
END
GO

DROP TRIGGER IF EXISTS IfCityExists
GO
CREATE TRIGGER IfCityExists ON Cities
INSTEAD OF INSERT
AS
BEGIN
	INSERT INTO Cities
	SELECT * FROM inserted
	WHERE city_id NOT IN (SELECT city_id FROM StoreTypes)
END
GO

DROP TRIGGER IF EXISTS IfStoreExists
GO
CREATE TRIGGER IfStoreExists ON Stores
INSTEAD OF INSERT
AS
BEGIN
	INSERT INTO Stores
	SELECT * FROM inserted
	WHERE store_id NOT IN (SELECT store_id FROM Stores)
END
GO

DROP TRIGGER IF EXISTS IfProductExists
GO
CREATE TRIGGER IfProductExists ON Products
INSTEAD OF INSERT
AS
BEGIN
	INSERT INTO Products
	SELECT * FROM inserted
	WHERE product_id NOT IN (SELECT product_id FROM Products)
END
GO

DROP TRIGGER IF EXISTS IfParametersExists
GO
CREATE TRIGGER IfParametersExists ON LossFunctionParameters
INSTEAD OF INSERT
AS
BEGIN
	INSERT INTO LossFunctionParameters(product_id, store_id,
		loyalty_charge_x, loyalty_charge_coef, storage_cost_coef,
		bank_rate_x, bank_rate_coef, product_cost_x, product_cost_coef)
	SELECT product_id, store_id,
		loyalty_charge_x, loyalty_charge_coef, storage_cost_coef,
		bank_rate_x, bank_rate_coef, product_cost_x, product_cost_coef FROM inserted
	WHERE CONCAT(product_id, store_id) NOT IN (SELECT CONCAT(product_id, store_id) FROM LossFunctionParameters)
END
GO