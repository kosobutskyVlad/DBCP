from typing import Optional

import pyodbc
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-stores")
def get_stores():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM Stores")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Stores": data}

@router.get("/get-store/{store_id}")
def get_store(store_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Stores WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{store_id} not found")

@router.post("/add-store/{store_id}")
def add_store(store_id: str, storetype_id: str, store_size: int, city_id: str):

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
    
    if data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{store_id} already exists")

    cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{city_id} does not exist")

    cursor.execute(f"SELECT storetype_id FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{storetype_id} does not exist")

    cursor.execute(f"INSERT INTO Stores VALUES('{store_id}', '{storetype_id}', '{store_size}', '{city_id}')")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "storetype_id": storetype_id, "store_size": store_size, "city_id": city_id}

@router.put("/update-store/{store_id}")
def update_store(store_id: str, storetype_id: Optional[str] = None,
                store_size: Optional[int] = None, city_id: Optional[str] = None):

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
        raise HTTPException(status_code=404, detail=f"{store_id} not found")

    update_values = []
    if storetype_id is not None:
        update_values.append(f"storetype_id = '{storetype_id}'")
        cursor.execute(f"SELECT storetype_id FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
        data = []
        for row in cursor:
            data.append(list(row))
    
        if not data:
            conn.close()
            raise HTTPException(status_code=422, detail=f"{storetype_id} does not exist")
    if store_size is not None:
        update_values.append(f"store_size = '{store_size}'")
    if city_id is not None:
        update_values.append(f"city_id = '{city_id}'")
        cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
        data = []
        for row in cursor:
            data.append(list(row))
    
        if not data:
            conn.close()
            raise HTTPException(status_code=422, detail=f"{city_id} does not exist")
    if not update_values:
        conn.close()
        raise HTTPException(status_code=422, detail=f"At least one field must be specified")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Stores SET {', '.join(update_values)} WHERE store_id = '{store_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Stores WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-store/{store_id}")
def delete_store(store_id: str):

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
        raise HTTPException(status_code=404, detail=f"{store_id} not found")

    cursor.execute(f"DELETE FROM Stores WHERE store_id = '{store_id}'")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "is_deleted": True}