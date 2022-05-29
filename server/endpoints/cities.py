from typing import List

from pydantic import BaseModel, constr
from fastapi import APIRouter

from sql_utils import get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Cities"
ID_FIELD = "city_id"

class City(BaseModel):
    city_id: constr(curtail_length=4)
    city_name: constr(curtail_length=50) = ""
    city_size: constr(curtail_length=10) = ""
    country: constr(curtail_length=50) = ""

router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
    responses={404: {"description": "Not found"}})

@router.get("/get-cities")
def get_cities() -> List:
    return select_eq(TABLE_NAME, [ID_FIELD])

@router.get("/get-city/{city_id}")
def get_city(city_id: str) -> List[List]:
    where_clause = get_where_clause([ID_FIELD], [city_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-city")
def add_city(city: City) -> dict:
    return insert(TABLE_NAME, city, ID_FIELD)

@router.put("/update-city")
def update_city(city: City) -> dict:
    return update(TABLE_NAME, ID_FIELD, city)

@router.delete("/delete-city/{city_id}")
def delete_city(city_id: str) -> dict:
    return delete(TABLE_NAME, ID_FIELD, city_id)