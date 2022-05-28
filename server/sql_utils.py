import pyodbc

CONNSTRING = ("Driver={SQL Server Native Client 11.0};"
              "Server=DESKTOP-P8N0IJI;"
              "Database=retail;"
              "Trusted_Connection=yes;")

def add_quotes(field_val):
    """
    Encloses string with single quotes if field_val is of str type
    """
    if type(field_val) == str:
        return f"'{field_val}'"
    return field_val
    

def exists(table_name: str, field_name: str, field_val) -> bool:
    """
    Returns True if there is a record in a table where field_name
    equals field_val
    """
    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {field_name} FROM {table_name} "
            f"WHERE {field_name} = {add_quotes(field_val)}"
        )
        data = []
        for row in cursor:
            data.append(row[0])
    return bool(data)

def is_referenced(table_name: str, field_name: str, field_val) -> bool:
    """
    Returns True if the record with field_name equals to field_val is
    being referenced by a foreign key
    """
    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {table_name} WHERE "
                           f"{field_name} = {add_quotes(field_val)}")
        except pyodbc.IntegrityError:
            return True
        return False