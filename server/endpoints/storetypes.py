from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class StoreType(BaseModel):
    storetype_id: str
    storetype_description: Optional[str] = None

router = APIRouter(
    prefix="/storetypes",
    tags=["Storetypes"],
    responses={404: {"description": "Not found"}})

@router.get("/get-storetypes")
def get_storetypes():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"storetypes": data}

@router.get("/get-storetype/{storetype_id}")
def get_storetype(storetype_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM StoreTypes \
                   WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404,
                        detail=f"{storetype_id} not found")

@router.post("/add-storetype")
def add_storetype(storetype: StoreType):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes \
                   WHERE storetype_id = '{storetype.storetype_id[:4]}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{storetype.storetype_id[:4]} \
                            already exists")

    cursor.execute(f"INSERT INTO StoreTypes \
                   VALUES('{storetype.storetype_id[:4]}', \
                   '{storetype.storetype_description[:100]}')")
    conn.commit()
    conn.close()
    return {"storetype_id": storetype.storetype_id[:4],
            "storetype_description":
            storetype.storetype_description[:100]}

@router.put("/update-storetype")
def update_storetype(storetype: StoreType):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes \
                   WHERE storetype_id = '{storetype.storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{storetype.storetype_id} \
                            not found")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE StoreTypes SET \
                   storetype_description = \
                   '{storetype.storetype_description[:100]}' \
                   WHERE storetype_id = '{storetype.storetype_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM StoreTypes \
                   WHERE storetype_id = '{storetype.storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-storetype/{storetype_id}")
def delete_storetype(storetype_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes \
                   WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{storetype_id} not found")

    cursor.execute(f"DELETE FROM StoreTypes \
                   WHERE storetype_id = '{storetype_id}'")
    conn.commit()
    conn.close()
    return {"storetype_id": storetype_id, "is_deleted": True}