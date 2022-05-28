from typing import Optional, List

from pydantic import BaseModel, constr
from fastapi import APIRouter

from sql_requests import select_ids, select_eq, insert, update, delete

TABLE_NAME = "Cities"
ID_NAME = "city_id"

class City(BaseModel):
    city_id: constr(curtail_length=4)
    city_name: Optional[constr(curtail_length=50)] = ""
    city_size: Optional[constr(curtail_length=10)] = ""
    country: Optional[constr(curtail_length=50)] = ""

router = APIRouter(
    prefix="/cities",
    tags=[TABLE_NAME],
    responses={404: {"description": "Not found"}})

@router.get("/get-cities")
def get_cities() -> List:
    return select_ids(TABLE_NAME, ID_NAME)

@router.get("/get-city/{city_id}")
def get_city(city_id: str) -> List[List]:
    return select_eq(TABLE_NAME, ID_NAME, city_id)

@router.post("/add-city")
def add_city(city: City) -> dict:
    return insert(TABLE_NAME, ID_NAME, city)

@router.put("/update-city")
def update_city(city: City) -> dict:
    return update(TABLE_NAME, ID_NAME, city)

@router.delete("/delete-city/{city_id}")
def delete_city(city_id: str) -> dict:
    return delete(TABLE_NAME, ID_NAME, city_id)