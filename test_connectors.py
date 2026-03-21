import os
from connectors.sqlite_connector import SQLiteConnector
from connectors.csv_connector import CSVConnector

DB_PATH = "data/database.db"
CSV_FOLDER = "data"

def test_connectors():
    """Тестирует коннекторы на .db и CSV файлах"""

    if os.path.exists(DB_PATH):
        sqlite_conn = SQLiteConnector(
            source_id="db_test",    
            name="Тестовая SQLite база", 
            db_path=DB_PATH        
        )
        
        tables = sqlite_conn.get_all_tables()
        print(f"get_all_tables(): {tables}")
        
        schema = sqlite_conn.get_schema()
        print(f"get_schema():")
        print(schema)
        
        print(f"get_sample_data():")
        for table in tables:
            data = sqlite_conn.get_sample_data(table,3)
            print(data)
    else:
        print(f"Файл {DB_PATH} не найден")
    
    print("\n CSVConnector (папка date)")
    
    if os.path.exists(CSV_FOLDER):
        csv_conn = csv_conn = CSVConnector(
            source_id="csv_test",   
            name="Тестовые CSV файлы",  
            folder_path=CSV_FOLDER  
        )
        
        tables = csv_conn.get_all_tables()
        print(f"get_all_tables(): {tables}")
        
        schema = csv_conn.get_schema()
        print(schema)
        
        print(f"get_sample_data():")
        for table in tables:
            data = csv_conn.get_sample_data(table,2)
            print(data)
    else:
        print(f"Папка {CSV_FOLDER} не найдена")


if __name__ == "__main__":
    test_connectors()