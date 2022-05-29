from typing import List

from pydantic import BaseModel, constr
from fastapi import APIRouter, HTTPException

from sql_utils import exists, get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Stores"
ID_FIELD = "store_id"

class Store(BaseModel):
    store_id: constr(curtail_length=5)
    storetype_id: constr(curtail_length=4) = ""
    city_id: constr(curtail_length=4) = ""
    store_size: int = 0

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
    responses={404: {"description": "Not found"}})

@router.get("/get-stores")
def get_stores() -> List:
    return select_eq(TABLE_NAME, [ID_FIELD])

@router.get("/get-store/{store_id}")
def get_store(store_id: str) -> List[List]:
    where_clause = get_where_clause([ID_FIELD], [store_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-store")
def add_store(store: Store) -> dict:
    
    if not exists("Cities", ["city_id"], [store.city_id]):
        raise HTTPException(status_code=422,
                            detail=f"{store.city_id} does not exist.")
        
    if not exists("StoreTypes", ["storetype_id"], [store.storetype_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{store.storetype_id} does not exist."
        )
        
    return insert(TABLE_NAME, store, ID_FIELD)

@router.put("/update-store")
def update_store(store: Store):

    if not exists("Cities", ["city_id"], [store.city_id]):
        raise HTTPException(status_code=422,
                            detail=f"{store.city_id} does not exist.")
        
    if not exists("StoreTypes", ["storetype_id"], [store.storetype_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{store.storetype_id} does not exist."
        )
        
    return update(TABLE_NAME, ID_FIELD, store)

@router.delete("/delete-store/{store_id}")
def delete_store(store_id: str):
    return delete(TABLE_NAME, ID_FIELD, store_id)