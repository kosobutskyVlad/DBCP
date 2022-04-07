from fastapi import APIRouter, HTTPException
from typing import Optional
import pyodbc

router = APIRouter(
    prefix="/cities",
    tags=["City"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get-cities")
def get_cities():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"cities": data}

@router.get("/get-city/{city_id}")
def get_city(city_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{city_id} not found")

@router.post("/add-city/{city_id}")
def get_city(city_id: str, city_name: str, city_size: str, country: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422, detail=f"{city_id} already exists")

    cursor.execute(f"INSERT INTO Cities VALUES('{city_id}', '{city_name}', '{city_size}', '{country}')")
    conn.commit()
    conn.close()
    return {"city_id": city_id, "city_name": city_name, "city_size": city_size, "country": country}

@router.put("/update-city/{city_id}")
def update_city(city_id: str, city_name: Optional[str] = None,
                city_size: Optional[str] = None, country: Optional[str] = None):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{city_id} not found")

    update_values = []
    if city_name is not None:
        update_values.append(f"city_name = '{city_name}'")
    if city_size is not None:
        update_values.append(f"city_size = '{city_size}'")
    if country is not None:
        update_values.append(f"country = '{country}'")
    if not update_values:
        conn.close()
        raise HTTPException(status_code=422, detail=f"At least one field must be specified")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Cities SET {', '.join(update_values)} WHERE city_id = '{city_id}'")
    conn.commit()

    cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}

@router.delete("/delete-city/{city_id}")
def delete_city(city_id: str):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404, detail=f"{city_id} not found")

    cursor.execute(f"DELETE FROM Cities WHERE city_id = '{city_id}'")
    conn.commit()
    conn.close()
    return {"city_id": city_id, "is_deleted": True}