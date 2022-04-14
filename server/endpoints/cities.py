from typing import Optional

import pyodbc
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class City(BaseModel):
    city_id: str
    city_name: Optional[str] = None
    city_size: Optional[str] = None
    country: Optional[str] = None

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}})

@router.get("/get-cities")
def get_cities():
    
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

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
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Cities WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))
    conn.close()

    if data:
        return {"Data": data}

    raise HTTPException(status_code=404, detail=f"{city_id} not found.")

@router.post("/add-city")
def add_city(city: City):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities \
                    WHERE city_id = '{city.city_id[:4]}'")
    data = []
    for row in cursor:
        data.append(list(row))
    
    if data:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"{city.city_id[:4]} already exists.")

    cursor.execute(f"INSERT INTO Cities VALUES('{city.city_id[:4]}', \
                   '{city.city_name[:50]}', '{city.city_size[:10]}', \
                   '{city.country[:50]}')")
    conn.commit()
    conn.close()
    return {"city_id": city.city_id[:4],
            "city_name": city.city_name[:50],
            "city_size": city.city_size[:10],
            "country": city.country[:50]}

@router.put("/update-city")
def update_city(city: City):

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities \
                   WHERE city_id = '{city.city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{city.city_id} not found.")

    update = []
    if city.city_name is not None:
        update.append(f"city_name = '{city.city_name[:50]}'")
    if city.city_size is not None:
        update.append(f"city_size = '{city.city_size[:10]}'")
    if city.country is not None:
        update.append(f"country = '{city.country[:50]}'")
    if not update:
        conn.close()
        raise HTTPException(status_code=422,
                            detail=f"Fill at least one field.")

    cursor = conn.cursor()
    cursor.execute(f"UPDATE Cities SET {', '.join(update)} \
                   WHERE city_id = '{city.city_id}'")
    conn.commit()

    cursor.execute(f"SELECT * FROM Cities \
                   WHERE city_id = '{city.city_id}'")
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
        "Trusted_Connection=yes;")

    cursor = conn.cursor()
    cursor.execute(f"SELECT city_id FROM Cities \
                   WHERE city_id = '{city_id}'")
    data = []
    for row in cursor:
        data.append(list(row))

    if not data:
        conn.close()
        raise HTTPException(status_code=404,
                            detail=f"{city_id} not found.")
    try:
        cursor.execute(f"DELETE FROM Cities WHERE city_id = '{city_id}'")
        conn.commit()
    except pyodbc.IntegrityError:
        raise HTTPException(status_code=409,
                            detail=f"{city_id} is being referenced by a foreign key.")
    finally:
        conn.close()

    return {"city_id": city_id, "is_deleted": True}