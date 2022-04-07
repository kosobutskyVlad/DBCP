CREATE DATABASE retail;

USE retail;

DROP TABLE IF EXISTS StoreTypes;
CREATE TABLE StoreTypes (
	storetype_id CHAR(4) PRIMARY KEY,
	storetype_description VARCHAR(100)
);

DROP TABLE IF EXISTS Cities;
CREATE TABLE Cities (
	city_id CHAR(4) PRIMARY KEY,
	city_name VARCHAR(50),
	city_size VARCHAR(10),
	country VARCHAR(50)
);

DROP TABLE IF EXISTS Stores;
CREATE TABLE Stores (
	store_id CHAR(5) PRIMARY KEY,
	storetype_id CHAR(4),
	store_size INT,
	city_id CHAR(4)
	CONSTRAINT FK_Store_StoreType FOREIGN KEY (storetype_id) REFERENCES StoreTypes(storetype_id),
	CONSTRAINT FK_Store_City FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);

DROP TABLE IF EXISTS Products;
CREATE TABLE Products (
	product_id CHAR(5) PRIMARY KEY,
	product_name VARCHAR(50),
	hierarchy_code CHAR(11),
	price FLOAT,
	product_length FLOAT,
	product_depth FLOAT,
	product_width FLOAT
);

DROP TABLE IF EXISTS LossFunctionParameters;
CREATE TABLE LossFunctionParameters (
	parameters_id INT PRIMARY KEY IDENTITY(1, 1),
	store_id CHAR(5),
	product_id CHAR(5),
	loyalty_charge_x FLOAT,
	loyalty_charge_coef FLOAT,
	storage_cost_coef FLOAT,
	bank_rate_x FLOAT,
	bank_rate_coef FLOAT,
	product_cost_x FLOAT,
	product_cost_coef FLOAT,
	CONSTRAINT FK_Parameter_Product FOREIGN KEY (product_id) REFERENCES Products(product_id),
	CONSTRAINT FK_Parameter_Store FOREIGN KEY (store_id) REFERENCES Stores(store_id)
);

DROP TABLE IF EXISTS Purchases;
CREATE TABLE Purchases (
	purchase_id INT PRIMARY KEY IDENTITY(1, 1),
	purchase_date DATE,
	product_id CHAR(5),
	store_id CHAR(5),
	price FLOAT,
	sales INT,
	discount FLOAT,
	revenue FLOAT,
	CONSTRAINT FK_Purchase_Product FOREIGN KEY (product_id) REFERENCES Products(product_id),
	CONSTRAINT FK_Purchase_Store FOREIGN KEY (store_id) REFERENCES Stores(store_id)
);