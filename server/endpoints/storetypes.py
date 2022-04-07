from fastapi import APIRouter, HTTPException
import pyodbc

router = APIRouter(
    prefix="/storetypes",
    tags=["Storetypes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-storetypes")
def get_storetypes():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

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
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{storetype_id} not found")

@router.post("/add-storetype/{storetype_id}")
def add_storetype(storetype_id: str, storetype_description: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{storetype_id} already exists")

    cursor.execute(f"INSERT INTO StoreTypes VALUES('{storetype_id}', '{storetype_description}')")
    conn.commit()
    conn.close()
    return {"storetype_id": storetype_id, "storetype_description": storetype_description}

@router.put("/update-storetype/{storetype_id}")
def update_storetype(storetype_id: str, storetype_description: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{storetype_id} not found")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE StoreTypes SET storetype_description = '{storetype_description}' WHERE storetype_id = '{storetype_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
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
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT storetype_id FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{storetype_id} not found")

    cursor.execute(f"DELETE FROM StoreTypes WHERE storetype_id = '{storetype_id}'")
    conn.commit()
    conn.close()
    return {"storetype_id": storetype_id, "is_deleted": True}