from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class Store(BaseModel):
    store_id: str
    storetype_id: Optional[str] = None
    city_id: Optional[str] = None
    store_size: Optional[int] = None

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
    responses={404: {"description": "Not found"}})

@router.get("/get-stores")
def get_stores():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM Stores")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"stores": data}

@router.get("/get-store/{store_id}")
def get_store(store_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Stores \
                   WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{store_id} not found")

@router.post("/add-store")
def add_store(store: Store):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{store.store_id[:5]}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{store.store_id[:5]} \
                            already exists")

    cursor.execute(f"SELECT city_id FROM Cities \
                   WHERE city_id = '{store.city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{store.city_id} does not exist")

    cursor.execute(f"SELECT storetype_id FROM StoreTypes \
                   WHERE storetype_id = '{store.storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if not data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{store.storetype_id} \
                            does not exist")

    cursor.execute(f"INSERT INTO Stores VALUES('{store.store_id[:5]}', \
                   '{store.storetype_id}', '{store.city_id}', \
                   '{store.store_size}')")
    conn.commit()
    conn.close()
    return {"store_id": store.store_id[:5],
            "storetype_id": store.storetype_id,
            "city_id": store.city_id,
            "store_size": store.store_size}

@router.put("/update-store")
def update_store(store: Store):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{store.store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{store.store_id} not found")

    update = []
    if store.storetype_id is not None:
        update.append(f"storetype_id = '{store.storetype_id[:4]}'")
        cursor.execute(f"SELECT storetype_id FROM StoreTypes \
                       WHERE storetype_id = '{store.storetype_id[:4]}'")
        data = []
        for row in cursor:
            data.append(list(row))
    
        if not data:
            conn.close()
            raise HTTPException(status_code=422,
                                detail=f"{store.storetype_id[:4]} \
                                does not exist")

    if store.city_id is not None:
        update.append(f"city_id = '{store.city_id[:4]}'")
        cursor.execute(f"SELECT city_id FROM Cities \
                       WHERE city_id = '{store.city_id[:4]}'")
        data = []
        for row in cursor:
            data.append(list(row))
    
        if not data:
            conn.close()
            raise HTTPException(status_code=422,
                                detail=f"{store.city_id[:4]} \
                                does not exist")
    if store.store_size is not None:
        update.append(f"store_size = '{store.store_size}'")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Stores SET {', '.join(update)} \
                   WHERE store_id = '{store.store_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Stores \
                   WHERE store_id = '{store.store_id}'")
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
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT store_id FROM Stores \
                   WHERE store_id = '{store_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{store_id} not found")

    cursor.execute(f"DELETE FROM Stores WHERE store_id = '{store_id}'")
    conn.commit()
    conn.close()
    return {"store_id": store_id, "is_deleted": True}