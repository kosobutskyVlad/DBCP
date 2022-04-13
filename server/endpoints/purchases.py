from datetime import date
from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class Purchase(BaseModel):
    store_id: str
    product_id: str
    purchase_date: Optional[date] = None
    price: Optional[float] = None
    sales: Optional[int] = None
    discount: Optional[float] = None
    revenue: Optional[float] = None

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
    responses={404: {"description": "Not found"}})

@router.get("/get-purchases-all")
def get_purchases_all():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id FROM Purchases")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"purchases": data}

@router.get("/get-purchases")
def get_purchases(store_id: Optional[str] = None, product_id: Optional[str] = None):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    where_clause = ""
    where_conditions = []
    if store_id:
        where_conditions.append(f"store_id = '{store_id}'")
    if product_id:
        where_conditions.append(f"product_id = '{product_id}'")
    if where_conditions:
        where_clause = " AND ".join(where_conditions)
    else:
        raise HTTPException(status_code=422,
                        detail=f"Specify at least one of: store_id; product_id")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM LossFunctionParameters \
                   WHERE {where_clause}")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"purchases": data}

    raise HTTPException(status_code=404,
                        detail=f"{store_id} and {product_id} \
                        not found")

@router.get("/get-purchase")
def get_purchases(purchase_id: int):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM LossFunctionParameters \
                   WHERE purchase_id = {purchase_id}")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{purchase_id} not found")

@router.post("/add-purchase")
def add_purchase(purchase: Purchase):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()

    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{purchase.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{purchase.store_id} \
                            does not exist")

    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{purchase.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{purchase.product_id} \
                            does not exist")

    cursor.execute(f"SELECT store_id, product_id FROM Purchases \
                   WHERE store_id = '{purchase.store_id}' \
                   AND product_id = '{purchase.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{purchase.store_id} \
                            and {purchase.product_id} \
                            already exists")

    cursor.execute(f"INSERT INTO Purchases(store_id, product_id, \
                   purchase_date, price, sales, discount, \
                   revenue) VALUES('{purchase.store_id}', \
                   '{purchase.product_id}', \
                   '{purchase.purchase_date}', \
                   '{purchase.price}', \
                   '{purchase.sales}', \
                   '{purchase.discount}', \
                   '{purchase.revenue}')")
    conn.commit()
    conn.close()
    return {"store_id": purchase.store_id,
            "product_id": purchase.product_id,
            "purchase_date": purchase.purchase_date,
            "price": purchase.price,
            "sales": purchase.sales,
            "discount": purchase.discount,
            "revenue": purchase.revenue}

@router.put("/update-purchase")
def update_purchase(purchase_id: int, purchase: Purchase):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT purchase_id \
                   FROM Purchases \
                   WHERE purchase_id = {purchase_id}")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{purchase_id} \
                            not found")
    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{purchase.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{purchase.store_id} \
                            does not exist")

    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{purchase.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{purchase.product_id} \
                            does not exist")

    update = []
    if purchase.store_id is not None:
        update.append(f"store_id = \
                      '{purchase.store_id}'")
    if purchase.product_id is not None:
        update.append(f"product_id = \
                      '{purchase.product_id}'")
    if purchase.purchase_date is not None:
        update.append(f"purchase_date = \
                      '{purchase.purchase_date}'")
    if purchase.price is not None:
        update.append(f"price = \
                      {purchase.price}")
    if purchase.sales is not None:
        update.append(f"sales = \
                      {purchase.sales}")
    if purchase.discount is not None:
        update.append(f"discount = \
                      {purchase.discount}")
    if purchase.revenue is not None:
        update.append(f"revenue = \
                      {purchase.revenue}")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Purchases \
                   SET {', '.join(update)} \
                   WHERE store_id = '{purchase.store_id}' \
                   AND product_id = '{purchase.product_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM LossFunctionParameters \
                   WHERE store_id = '{purchase.store_id}' \
                   AND product_id = '{purchase.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-purchase/{purchase_id}")
def delete_purchase(purchase_id: int):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT purchase_id FROM Purchases \
                   WHERE purchase_id = '{purchase_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{purchase_id} not found")

    cursor.execute(f"DELETE FROM Purchases \
                   WHERE purchase_id = '{purchase_id}'")
    conn.commit()
    conn.close()
    return {"purchase_id": purchase_id, "is_deleted": True}