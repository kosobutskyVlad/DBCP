from typing import Optional, List

from pydantic import BaseModel, constr
from fastapi import APIRouter

from sql_requests import select_ids, select_eq, insert, update, delete

TABLE_NAME = "Storetypes"
ID_NAME = "storetype_id"

class StoreType(BaseModel):
    storetype_id: constr(curtail_length=4)
    storetype_description: Optional[constr(curtail_length=100)] = ""

router = APIRouter(
    prefix="/storetypes",
    tags=["Storetypes"],
    responses={404: {"description": "Not found"}})

@router.get("/get-storetypes")
def get_storetypes() -> List:
    return select_ids(TABLE_NAME, ID_NAME)

@router.get("/get-storetype/{storetype_id}")
def get_storetype(storetype_id: str) -> List[List]:
    return select_eq(TABLE_NAME, ID_NAME, storetype_id)

@router.post("/add-storetype")
def add_storetype(storetype: StoreType) -> dict:
    return insert(TABLE_NAME, ID_NAME, storetype)

@router.put("/update-storetype")
def update_storetype(storetype: StoreType) -> dict:
    return update(TABLE_NAME, ID_NAME, storetype)

@router.delete("/delete-storetype/{storetype_id}")
def delete_storetype(storetype_id: str) -> dict:
    return delete(TABLE_NAME, ID_NAME, storetype_id)