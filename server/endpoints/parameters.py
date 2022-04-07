from fastapi import APIRouter, HTTPException
from typing import Optional
import pyodbc

router = APIRouter(
    prefix="/parameters",
    tags=["Parameters"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-parameters-all")
def get_parameters_all():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id FROM LossFunctionParameters")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"parameters": data}

@router.get("/get-parameters")
def get_parameters(store_id: str, product_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{store_id} and {product_id} co-occurrence not found")

@router.post("/add-parameters")
def add_parameters(store_id: str, product_id: str, loyalty_charge_x: float, loyalty_charge_coef: float,
                        storage_cost_coef: float, bank_rate_x: float,
                        bank_rate_coef: float, product_cost_x: float,
                        product_cost_coef: float):

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

    cursor.execute(f"SELECT store_id, product_id FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{store_id} and {product_id} co-occurrence already exists")

    cursor.execute(f"INSERT INTO LossFunctionParameters(store_id, product_id, loyalty_charge_x, loyalty_charge_coef, \
                        storage_cost_coef, bank_rate_x, \
                        bank_rate_coef, product_cost_x, \
                        product_cost_coef) VALUES('{store_id}', '{product_id}', \
                        '{loyalty_charge_x}', '{loyalty_charge_coef}', '{storage_cost_coef}', \
                        '{bank_rate_x}', '{bank_rate_coef}', '{product_cost_x}', '{product_cost_coef}')")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "product_id": product_id, "loyalty_charge_x": loyalty_charge_x,
            "loyalty_charge_coef": loyalty_charge_coef, "storage_cost_coef": storage_cost_coef,
            "bank_rate_x": bank_rate_x, "bank_rate_coef": bank_rate_coef,
            "product_cost_x": product_cost_x, "product_cost_coef": product_cost_coef}

@router.put("/update-parameters")
def update_parameters(store_id: str, product_id: str,
                        loyalty_charge_x: Optional[float] = None,
                        loyalty_charge_coef: Optional[float] = None,
                        storage_cost_coef: Optional[float] = None, bank_rate_x: Optional[float] = None,
                        bank_rate_coef: Optional[float] = None, product_cost_x: Optional[float] = None,
                        product_cost_coef: Optional[float] = None):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{store_id} and {product_id} co-occurrence not found")

    update_values = []
    if loyalty_charge_x is not None:
        update_values.append(f"loyalty_charge_x = '{loyalty_charge_x}'")
    if loyalty_charge_coef is not None:
        update_values.append(f"loyalty_charge_coef = '{loyalty_charge_coef}'")
    if storage_cost_coef is not None:
        update_values.append(f"storage_cost_coef = '{storage_cost_coef}'")
    if bank_rate_x is not None:
        update_values.append(f"bank_rate_x = '{bank_rate_x}'")
    if bank_rate_coef is not None:
        update_values.append(f"bank_rate_coef = '{bank_rate_coef}'")
    if product_cost_x is not None:
        update_values.append(f"product_cost_x = '{product_cost_x}'")
    if product_cost_coef is not None:
        update_values.append(f"product_cost_coef = '{product_cost_coef}'")
    if not update_values:
        conn.close()
        raise HTTPException(status_code=422, detail=f"At least one field must be specified")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE LossFunctionParameters SET {', '.join(update_values)} WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-parameters")
def delete_parameters(store_id: str, product_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{store_id} and {product_id} co-occurrence not found")

    cursor.execute(f"DELETE FROM LossFunctionParameters WHERE store_id = '{store_id}' AND product_id = '{product_id}'")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "product_id": product_id, "is_deleted": True}