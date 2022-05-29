from typing import List

from pydantic import BaseModel, constr, confloat
from fastapi import APIRouter

from sql_utils import get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Products"
ID_FIELD = "product_id"

class Product(BaseModel):
    product_id: constr(curtail_length=5)
    product_name: constr(curtail_length=50)
    hierarchy_code: constr(curtail_length=11) = ""
    price: confloat(gt=0) = 0.01
    product_length: confloat(gt=0) = 0.01
    product_depth: confloat(gt=0) = 0.01
    product_width: confloat(gt=0) = 0.01

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}})

@router.get("/get-products")
def get_products() -> List:
    return select_eq(TABLE_NAME, [ID_FIELD])

@router.get("/get-product/{product_id}")
def get_product(product_id: str) -> List[List]:
    where_clause = get_where_clause([ID_FIELD], [product_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.get("/get-by-storeid")
def get_product_by_storeid(store_id: str) -> List[List]:
    where_clause = get_where_clause(["store_id"], [store_id])
    return select_eq("LossFunctionParameters", ["product_id"],
                     where_clause, True)

@router.post("/add-product")
def add_product(product: Product) -> dict:
    return insert(TABLE_NAME, product, ID_FIELD)

@router.put("/update-product")
def update_product(product: Product) -> dict:
    return update(TABLE_NAME, ID_FIELD, product)

@router.delete("/delete-product/{product_id}")
def delete_product(product_id: str) -> dict:
    return delete(TABLE_NAME, ID_FIELD, product_id)