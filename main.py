import os
from connectors import CSVConnector, SQLiteConnector
from index import MetadataIndex
from search import SearchEngine
from mcp import MCPTools
from ui.cli import CLI

def setup_demo_data():
    """Проверяет наличие источников данных в папке data и выводит информацию о них"""
    
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"Папка '{data_dir}' не найдена!")
        return False
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if csv_files:
        print(f"Найдены CSV файлы в папке '{data_dir}':")
        for csv_file in csv_files:
            print(f"  - {csv_file}")
    else:
        print(f"CSV файлы не найдены в папке '{data_dir}'")

    db_files = [f for f in os.listdir(data_dir) if f.endswith('.db')]
    if db_files:
        print(f"Найдены SQLite базы данных в папке '{data_dir}':")
        for db_file in db_files:
            print(f"  - {db_file}")
    else:
        print(f"SQLite базы данных не найдены в папке '{data_dir}'")
    
    return True

def main():
    # Проверяем наличие источников данных в папке data
    data_dir = "data"
    if not setup_demo_data():
        print("Нет данных для работы. Поместите файлы в папку 'data'")
        return

    metadata_index = MetadataIndex()
    
    # Добавляем коннекторы для CSV файлов
    print("\n Добавление источников данных...")
    # Находим все CSV файлы в папке data
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if csv_files:
        # Создаем один коннектор для всех CSV файлов в папке data
        csv_connector = CSVConnector(
            source_id="csv_source",
            name="CSV Файлы",
            folder_path=data_dir  
        )
        metadata_index.add_source("csv_source", csv_connector)
        print(f"Добавлен CSV источник: csv_source (найдено файлов: {len(csv_files)})")
    else:
        print("CSV файлы не найдены")
    
    # Находим SQLite базы данных в папке data
    db_files = [f for f in os.listdir(data_dir) if f.endswith('.db')]
    
    if db_files:
        # Для каждой найденной базы создаем отдельный коннектор
        for db_file in db_files:
            source_id = db_file.replace('.db', '_source')
            source_name = f"SQLite: {db_file}"
            
            sqlite_connector = SQLiteConnector(
                source_id=source_id,
                name=source_name,
                db_path=os.path.join(data_dir, db_file)  # Полный путь к файлу
            )
            metadata_index.add_source(source_id, sqlite_connector)
            print(f"Добавлен SQLite источник: {source_id} ({db_file})")
    else:
        print("SQLite базы данных не найдены")
    
    print("Индексация источников...")
    sources = metadata_index.list_sources()
    if not sources:
        print("Нет источников для индексации!")
        return
    
    indexed_count = 0
    for source in sources:
        if metadata_index.index_source(source['source_id']):
            indexed_count += 1
            print(f"Индексирован {source['name']}")
        else:
            print(f"Ошибка индексации {source['name']}")
    
    print(f"Проиндексировано {indexed_count} из {len(sources)} источников")
    
    search_engine = SearchEngine(metadata_index)
    mcp_tools = MCPTools(metadata_index, search_engine)
    
    print(" Система готова к работе")
    cli = CLI(mcp_tools)
    cli.run()

if __name__ == "__main__":
    main()