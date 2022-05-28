from typing import List, Optional

import pyodbc
from pydantic import BaseModel
from fastapi import HTTPException

from sql_utils import CONNSTRING, add_quotes, exists, is_referenced

def select_ids(table_name: str, field_name: str) -> List:
    """
    Returns IDs from a table
    """
    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT {field_name} FROM {table_name}")
            data = []
            for row in cursor:
                data.append(row[0])
    return data

def select_eq(table_name: str, field_name: str, field_val,
              fields: Optional[List[str]] = None,
              distinct: bool = False) -> List[List]:
    """
    Returns records where field_name equals field_val
    """

    fields_str = "*"
    if fields is not None:
        fields_str = ", ".join(fields)

    distinct_str = "DISTINCT" if distinct else ""

    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT {distinct_str} {fields_str} FROM {table_name} "
                f"WHERE {field_name} = {add_quotes(field_val)}"
            )
            data = []
            for row in cursor:
                data.append(list(row))
    return data

def insert(table_name: str, id_name: str, model: BaseModel) -> dict:
    item_id = getattr(model, id_name)
    if exists(table_name, id_name, item_id):
        raise HTTPException(
            status_code=422,
            detail=f"{item_id} already exists."
        )

    fields = []
    vals = []
    for field, val in model:
        fields.append(field)
        vals.append(add_quotes(val))
    
    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {table_name}({', '.join(fields)}) "
                f"VALUES({', '.join(vals)})"
            )

    return dict(model)

def update(table_name: str, id_name: str, model: BaseModel) -> dict:
    item_id = getattr(model, id_name)
    if not exists(table_name, id_name, item_id):
        raise HTTPException(
            status_code=404,
            detail=f"{item_id} not found."
        )
    
    update = []
    for field, val in model:
        if val:
            update.append(f"{field} = {add_quotes(val)}")
        
    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table_name} SET {', '.join(update)} "
                f"WHERE {id_name} = {add_quotes(item_id)}")

    return select_eq(table_name, id_name, item_id)

def delete(table_name: str, field_name: str, item_id: str) -> bool:
    item = select_eq(table_name, field_name, item_id)
    if not item:
        raise HTTPException(status_code=404,
                            detail=f"{item_id} not found.")

    if is_referenced(table_name, field_name, item_id):
        raise HTTPException(
            status_code=409,
            detail=f"{item_id} is being referenced by a foreign key."
        )

    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE "
                           f"{field_name} = {add_quotes(item_id)}")
    return item