from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class Stock(BaseModel):
    store_id: str
    product_id: str
    stock: int = 0

router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    responses={404: {"description": "Not found"}})


@router.get("/get-stock")
def get_stock_by_store(store_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Stock WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"stock": data}

    raise HTTPException(status_code=404,
                        detail=f"{store_id} stock not found.")

@router.get("/get-stock/{stock_id}")
def get_stock_by_id(stock_id: int):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Stock \
                   WHERE stock_id = {stock_id}")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{stock_id} not found.")

@router.post("/add-stock")
def add_stock(stock: Stock):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()

    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{stock.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{stock.store_id} \
                            does not exist")

    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{stock.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{stock.product_id} does not exist.")

    cursor.execute(f"INSERT INTO Purchases(store_id, product_id, \
                   stock) VALUES('{stock.store_id}', \
                   '{stock.product_id}', \
                   '{stock.stock}')")
    conn.commit()
    conn.close()
    return {"store_id": stock.store_id,
            "product_id": stock.product_id,
            "stock": stock.stock}

@router.put("/update-stock")
def update_stock(stock_id: int, stock: Stock):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT stock_id FROM Stock \
                   WHERE stock_id = {stock_id}")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{stock_id} not found.")
    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{stock.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{stock.store_id} \
                            does not exist")

    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{stock.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{stock.product_id} does not exist.")

    update = []
    if stock.store_id is not None:
        update.append(f"store_id = '{stock.store_id}'")
    if stock.product_id is not None:
        update.append(f"product_id = '{stock.product_id}'")
    if stock.stock is not None:
        update.append(f"stock = '{stock.stock}'")

    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field.")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Stock SET {', '.join(update)} \
                   WHERE stock_id = '{stock_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Stock WHERE stock_id = '{stock_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-stock/{stock_id}")
def delete_stock(stock_id: int):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT stock_id FROM Stock \
                   WHERE stock_id = '{stock_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{stock_id} not found.")

    cursor.execute(f"DELETE FROM Stock WHERE stock_id = '{stock_id}'")
    conn.commit()
    conn.close()
    return {"stock_id": stock_id, "is_deleted": True}