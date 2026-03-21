
"""
Демонстрация работы Data Discovery Tool
Показывает индексацию и поиск по источникам данных
"""

from connectors.sqlite_connector import SQLiteConnector
from connectors.csv_connector import CSVConnector
from index.metadata_index import MetadataIndex

def main():

    print("1. Создаю индекс метаданных...")
    index = MetadataIndex()
    
    print("2. Добавляю источники данных...")
    
    sqlite_conn = SQLiteConnector(
        source_id="sqlite_1",
        name="SQLite Database",
        db_path="data/database.db"  
    )
    index.add_source("sqlite_1", sqlite_conn)
    
    csv_conn = CSVConnector(
        source_id="csv_1",
        name="CSV Files",
        folder_path="data"  
    )
    index.add_source("csv_1", csv_conn)
    
    print("3. Индексирую источники...")
    index.index_source("sqlite_1")
    index.index_source("csv_1")
    
    print("4. Доступные источники:")
    for source in index.list_sources():
        print(f"  • {source['name']} (ID: {source['source_id']})")
    
    print("5. ПОИСК:")
    
    search_queries = ["employee", "name", "salary", "city", "bonus"]
    
    for query in search_queries:
        print(f"\n   Поиск: '{query}'")
        results = index.search(query)
        
        if results['tables']:
            print(f"      Найдено таблиц: {len(results['tables'])}")
            for table in results['tables']:
                print(f"      - {table['table_name']} (источник: {table['source_name']})")
        
        if results['columns']:
            print(f"      Найдено колонок: {len(results['columns'])}")
            for col in results['columns']:
                print(f"      - {col['column_name']} в таблице {col['table_name']}")
        
        if not results['tables'] and not results['columns']:
            print("      Ничего не найдено")
    
    print("6. ДЕТАЛЬНЫЙ ПРОСМОТР:")
    
    # Проверяем таблицы, которые есть в data
    tables_to_check = ["employees", "addresses", "performance"]
    
    for table_name in tables_to_check:
        schema = index.get_schema("csv_1", table_name)
        
        if schema:
            print(f"   Таблица: {schema['table_name']}")
            print(f"   Источник: {schema['source_name']}")
            print(f"   Колонки ({len(schema['columns'])}): {', '.join(schema['columns'])}")
            print(f"   Примеры данных (первые 3):")
            for i, row in enumerate(schema['sample_data'][:3], 1):
                print(f"      {i}. {row}")
        else:
            print(f"   Таблица '{table_name}' не найдена")

if __name__ == "__main__":
    main()