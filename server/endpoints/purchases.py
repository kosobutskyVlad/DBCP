from datetime import date
from typing import Optional

import pyodbc
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-purchases-all")
def get_purchases_all():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id FROM Purchases")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"purchases": data}

@router.get("/get-purchases")
def get_purchases(store_id: str, product_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Purchases WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{store_id} and {product_id} co-occurrence not found")

@router.post("/add-purchase")
def add_purchase(store_id: str, product_id: str, purchase_date: date, price: float,
                        sales: int, discount: float, revenue: float):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()

    cursor.execute(f"SELECT store_id FROM Stores WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{store_id} does not exist")

    cursor.execute(f"SELECT product_id FROM Products WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{product_id} does not exist")

    cursor.execute(f"SELECT store_id, product_id FROM Purchases WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{store_id} and {product_id} co-occurrence already exists")

    cursor.execute(f"INSERT INTO Purchases(store_id, product_id, purchase_date, price, \
                        sales, discount, \
                        revenue) VALUES('{store_id}', '{product_id}', \
                        '{purchase_date}', '{price}', '{sales}', \
                        '{discount}', '{revenue}')")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "product_id": product_id, "purchase_date": purchase_date,
            "price": price, "sales": sales, "discount": discount, "revenue": revenue}

@router.delete("/delete-purchase/{purchase_id}")
def delete_purchase(purchase_id: int):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT purchase_id FROM Purchases WHERE purchase_id = '{purchase_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{purchase_id} not found")

    cursor.execute(f"DELETE FROM Purchases WHERE purchase_id = '{purchase_id}'")
    conn.commit()
    conn.close()
    return {"purchase_id": purchase_id, "is_deleted": True}