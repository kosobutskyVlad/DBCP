from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class Product(BaseModel):
    product_id: str
    product_name: str
    hierarchy_code: Optional[str] = None
    price: Optional[float] = None
    product_length: Optional[float] = None
    product_depth: Optional[float] = None
    product_width: Optional[float] = None

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
                        detail=f"{product_id} not found.")

@router.get("/get-by-storeid")
def get_product_by_storeid(store_id: str):
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT product_id FROM LossFunctionParameters \
                   WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{store_id} not found.")

@router.post("/add-product")
def add_product(product: Product):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{product.product_id[:5]}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{product.product_id[:5]} already exists.")

    cursor.execute(f"INSERT INTO Products \
                   VALUES('{product.product_id[:5]}', \
                   '{product.product_name[:50]}', \
                   '{product.hierarchy_code[:10]}', \
                   '{product.price}', \
                   '{product.product_length}', \
                   '{product.product_depth}', \
                   '{product.product_width}')")
    conn.commit()
    conn.close()
    return {"product_id": product.product_id[:5],
            "product_description": product.product_name[:50],
            "hierarchy_code": product.hierarchy_code[:10],
            "price": product.price,
            "product_length": product.product_length,
            "product_depth": product.product_depth,
            "product_width": product.product_width}

@router.put("/update-product")
def update_product(product: Product):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{product.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{product.product_id} not found.")

    update = []
    if product.product_name is not None:
        update.append(f"product_name = '{product.product_name[:50]}'")
    if product.hierarchy_code is not None:
        update.append(f"hierarchy_code = \
                      '{product.hierarchy_code[:10]}'")
    if product.price is not None:
        update.append(f"price = '{product.price}'")
    if product.product_length is not None:
        update.append(f"product_length = '{product.product_length}'")
    if product.product_depth is not None:
        update.append(f"product_depth = '{product.product_depth}'")
    if product.product_width is not None:
        update.append(f"product_width = '{product.product_width}'")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field.")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Products SET {', '.join(update)} \
                   WHERE product_id = '{product.product_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Products \
                   WHERE product_id = '{product.product_id}'")
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
                            detail=f"{product_id} not found.")

    try:
        cursor.execute(f"DELETE FROM Products \
                   WHERE product_id = '{product_id}'")
        conn.commit()
    except pyodbc.IntegrityError:
        raise HTTPException(status_code=409,
                            detail=f"{product_id} is being referenced by a foreign key.")
    finally:
        conn.close()

    return {"product_id": product_id, "is_deleted": True}