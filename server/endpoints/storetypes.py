from typing import List

from pydantic import BaseModel, constr
from fastapi import APIRouter

from sql_utils import get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Storetypes"
ID_FIELD = "storetype_id"

class StoreType(BaseModel):
    storetype_id: constr(curtail_length=4)
    storetype_description: constr(curtail_length=100) = ""

router = APIRouter(
    prefix="/storetypes",
    tags=["Storetypes"],
    responses={404: {"description": "Not found"}})

@router.get("/get-storetypes")
def get_storetypes() -> List:
    return select_eq(TABLE_NAME, [ID_FIELD])

@router.get("/get-storetype/{storetype_id}")
def get_storetype(storetype_id: str) -> List[List]:
    where_clause = get_where_clause([ID_FIELD], [storetype_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-storetype")
def add_storetype(storetype: StoreType) -> dict:
    return insert(TABLE_NAME, storetype, ID_FIELD)

@router.put("/update-storetype")
def update_storetype(storetype: StoreType) -> dict:
    return update(TABLE_NAME, ID_FIELD, storetype)

@router.delete("/delete-storetype/{storetype_id}")
def delete_storetype(storetype_id: str) -> dict:
    return delete(TABLE_NAME, ID_FIELD, storetype_id)