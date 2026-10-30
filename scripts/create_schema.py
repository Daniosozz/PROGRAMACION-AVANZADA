"""Create database tables from the SQL schema file."""
from pathlib import Path
from sqlalchemy import text
from db_config import get_engine

def create_schema():
    engine = get_engine()
    sql_path = Path(__file__).resolve().parents[1] / "sql" / "01_create_tables.sql"
    
    if not sql_path.exists():
        raise FileNotFoundError(f"Could not find schema file at {sql_path}")
    
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
        
    with engine.begin() as connection:
        connection.execute(text(sql_script))
        print("Schema created (or existing tables found).")

if __name__ == "__main__":
    create_schema()
    