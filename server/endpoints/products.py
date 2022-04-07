from typing import Optional

import pyodbc
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}})

@router.get("/get-products")
def get_products():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Products")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"products": data}

@router.get("/get-product/{product_id}")
def get_product(product_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Products \
                   WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{product_id} not found")

@router.post("/add-product/{product_id}")
def add_product(product_id: str, product_name: str,
                hierarchy_code: str, price: float,
                product_length: float, product_depth: float,
                product_width: float):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{product_id} already exists")

    cursor.execute(f"INSERT INTO Products VALUES('{product_id}', \
                   '{product_name}', '{hierarchy_code}', '{price}', \
                   '{product_length}', '{product_depth}', \
                   '{product_width}')")
    conn.commit()
    conn.close()
    return {"product_id": product_id,
            "product_description": product_name,
            "hierarchy_code": hierarchy_code,
            "price": price,
            "product_length": product_length,
            "product_depth": product_depth,
            "product_width": product_width}

@router.put("/update-product/{product_id}")
def update_product(product_id: str,
                   product_name: Optional[str] = None,
                   hierarchy_code: Optional[str] = None,
                   price: Optional[float] = None,
                   product_length: Optional[float] = None,
                   product_depth: Optional[float] = None,
                   product_width: Optional[float] = None):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{product_id} not found")

    update = []
    if product_name is not None:
        update.append(f"product_name = '{product_name}'")
    if hierarchy_code is not None:
        update.append(f"hierarchy_code = '{hierarchy_code}'")
    if price is not None:
        update.append(f"price = '{price}'")
    if product_length is not None:
        update.append(f"product_length = '{product_length}'")
    if product_depth is not None:
        update.append(f"product_depth = '{product_depth}'")
    if product_width is not None:
        update.append(f"product_width = '{product_width}'")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Products SET {', '.join(update)} \
                   WHERE product_id = '{product_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Products \
                   WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-product/{product_id}")
def delete_product(product_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Product \
                    WHERE product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{product_id} not found")

    cursor.execute(f"DELETE FROM Products \
                   WHERE product_id = '{product_id}'")
    conn.commit()
    conn.close()
    return {"product_id": product_id, "is_deleted": True}