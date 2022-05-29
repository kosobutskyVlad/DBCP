from typing import Optional, List

from pydantic import BaseModel, constr, confloat
from fastapi import APIRouter, HTTPException

from sql_utils import exists, get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "LossFunctionParameters"
ID_FIELD = "parameters_id"

class Parameters(BaseModel):
    store_id: constr(curtail_length=5)
    product_id: constr(curtail_length=5)
    loyalty_charge_x: confloat(le=0) = 0
    loyalty_charge_coef: confloat(le=0) = 0
    storage_cost_coef: confloat(ge=0) = 0
    bank_rate_x: confloat(ge=0) = 0
    bank_rate_coef: confloat(ge=0) = 0
    product_cost_x: confloat(ge=0) = 0
    product_cost_coef: confloat(ge=0) = 0

router = APIRouter(
    prefix="/parameters",
    tags=["Parameters"],
    responses={404: {"description": "Not found"}})

@router.get("/get-parameters")
def get_parameters(store_id: Optional[str] = None,
                   product_id: Optional[str] = None) -> List[List]:
    where_clause = get_where_clause(
        ["store_id", "product_id"], [store_id, product_id]
    )
    if not where_clause:
        raise HTTPException(status_code=422,
                        detail=("Specify at least one of:"
                                "store_id or product_id."))
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.get("/get-parameters/{parameters_id}")
def get_parameters_by_id(parameters_id: str) -> List[List]:
    where_clause = get_where_clause(["parameters_id"], [parameters_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-parameters")
def add_parameters(parameters: Parameters) -> dict:
    if not exists("Stores", ["store_id"], [parameters.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{parameters.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [parameters.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{parameters.product_id} does not exist."
        )

    where_clause = get_where_clause(
        ["store_id", "product_id"],
        [parameters.store_id, parameters.product_id]
    )
    if select_eq(TABLE_NAME, ["parameters_id"], where_clause) != [[]]:
        raise HTTPException(
            status_code=422,
            detail=(f"{parameters.store_id} and {parameters.product_id}"
                    " already exists.")
        )

    return insert(TABLE_NAME, parameters)

@router.put("/update-parameters")
def update_parameters(parameters: Parameters) -> dict:
    if not exists("Stores", ["store_id"], [parameters.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{parameters.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [parameters.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{parameters.product_id} does not exist."
        )

    return update(TABLE_NAME, ID_FIELD, parameters)

@router.delete("/delete-parameters/{parameters_id}")
def delete_parameters(parameters_id: int) -> dict:
     return delete(TABLE_NAME, ID_FIELD, parameters_id)