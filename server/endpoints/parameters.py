from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class Parameters(BaseModel):
    store_id: str
    product_id: str
    loyalty_charge_x: Optional[float] = None
    loyalty_charge_coef: Optional[float] = None
    storage_cost_coef: Optional[float] = None
    bank_rate_x: Optional[float] = None
    bank_rate_coef: Optional[float] = None
    product_cost_x: Optional[float] = None
    product_cost_coef: Optional[float] = None

router = APIRouter(
    prefix="/parameters",
    tags=["Parameters"],
    responses={404: {"description": "Not found"}})

@router.get("/get-parameters-all")
def get_parameters_all():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id \
                   FROM LossFunctionParameters")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"parameters": data}

@router.get("/get-parameters")
def get_parameters(store_id: Optional[str] = None, product_id: Optional[str] = None):

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
                        detail=f"Specify at least one of: store_id or product_id.")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM LossFunctionParameters \
                   WHERE {where_clause}")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"parameters": data}

    raise HTTPException(status_code=404,
                        detail=f"{store_id} and {product_id} not found.")

@router.post("/add-parameters")
def add_parameters(parameters: Parameters):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()

    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{parameters.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{parameters.store_id} \
                            does not exist")

    cursor.execute(f"SELECT product_id FROM Products \
                   WHERE product_id = '{parameters.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{parameters.product_id} \
                            does not exist")

    cursor.execute(f"SELECT store_id, product_id \
                   FROM LossFunctionParameters \
                   WHERE store_id = '{parameters.store_id}' \
                   AND product_id = '{parameters.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{parameters.store_id[:5]} and {parameters.product_id[:5]} parameters already exist.")

    cursor.execute(f"INSERT INTO LossFunctionParameters( \
                   store_id, product_id, loyalty_charge_x, \
                   loyalty_charge_coef, storage_cost_coef, \
                   bank_rate_x, bank_rate_coef, product_cost_x, \
                   product_cost_coef) \
                   VALUES('{parameters.store_id[:5]}', \
                   '{parameters.product_id[:5]}', \
                   '{parameters.loyalty_charge_x}', \
                   '{parameters.loyalty_charge_coef}', \
                   '{parameters.storage_cost_coef}', \
                   '{parameters.bank_rate_x}', \
                   '{parameters.bank_rate_coef}', \
                   '{parameters.product_cost_x}', \
                   '{parameters.product_cost_coef}')")
    conn.commit()
    conn.close()
    return {"store_id": parameters.store_id[:5],
            "product_id": parameters.product_id[:5],
            "loyalty_charge_x": parameters.loyalty_charge_x,
            "loyalty_charge_coef": parameters.loyalty_charge_coef,
            "storage_cost_coef": parameters.storage_cost_coef,
            "bank_rate_x": parameters.bank_rate_x,
            "bank_rate_coef": parameters.bank_rate_coef,
            "product_cost_x": parameters.product_cost_x,
            "product_cost_coef": parameters.product_cost_coef}

@router.put("/update-parameters")
def update_parameters(parameters: Parameters):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id \
                   FROM LossFunctionParameters \
                   WHERE store_id = '{parameters.store_id}' \
                   AND product_id = '{parameters.product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{parameters.store_id} and {parameters.product_id} not found.")

    update = []
    if parameters.loyalty_charge_x is not None:
        update.append(f"loyalty_charge_x = \
                      '{parameters.loyalty_charge_x}'")
    if parameters.loyalty_charge_coef is not None:
        update.append(f"loyalty_charge_coef = \
                      '{parameters.loyalty_charge_coef}'")
    if parameters.storage_cost_coef is not None:
        update.append(f"storage_cost_coef = \
                      '{parameters.storage_cost_coef}'")
    if parameters.bank_rate_x is not None:
        update.append(f"bank_rate_x = \
                      '{parameters.bank_rate_x}'")
    if parameters.bank_rate_coef is not None:
        update.append(f"bank_rate_coef = \
                      '{parameters.bank_rate_coef}'")
    if parameters.product_cost_x is not None:
        update.append(f"product_cost_x = \
                      '{parameters.product_cost_x}'")
    if parameters.product_cost_coef is not None:
        update.append(f"product_cost_coef = \
                      '{parameters.product_cost_coef}'")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field.")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE LossFunctionParameters \
                   SET {', '.join(update)} \
                   WHERE store_id = '{parameters.store_id}' \
                   AND product_id = '{parameters.product_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM LossFunctionParameters \
                   WHERE store_id = '{parameters.store_id}' \
                   AND product_id = '{parameters.product_id}'")
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
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id, product_id \
                   FROM LossFunctionParameters \
                   WHERE store_id = '{store_id}' \
                   AND product_id = '{product_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{store_id} and {product_id} not found.")

    cursor.execute(f"DELETE FROM LossFunctionParameters \
                   WHERE store_id = '{store_id}' \
                   AND product_id = '{product_id}'")
    conn.commit()
    conn.close()
    return {"store_id": store_id,
            "product_id": product_id,
            "is_deleted": True}