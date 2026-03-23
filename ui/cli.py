from typing import Dict, Any
from mcp import MCPTools

class CLI:
    """Простой интерфейс командной строки"""
    
    def __init__(self, mcp_tools: MCPTools):
        self.mcp_tools = mcp_tools
    
    def print_help(self):
        """Выводит справку"""
        print("Data Discovery Tool - CLI")
        print("Доступные команды:")
        print("  list                    - Показать все источники данных")
        print("  index <source_id>       - Индексировать источник данных")
        print("  search <query>          - Поиск по ключевому слову")
        print("  schema <source_id> <table> - Показать схему таблицы")
        print("  help                    - Показать эту справку")
        print("  exit                    - Выйти")
    
    def print_search_results(self, results: Dict[str, Any]):
        """Выводит результаты поиска"""
        if not results['tables'] and not results['columns']:
            print("\n Ничего не найдено")
            return
        
        print("Результаты поиска:")
        if results['tables']:
            print("Таблицы:")
            for table in results['tables']:
                print(f" >{table['table_name']} (источник: {table['source_name']})")
        
        if results['columns']:
            print("Колонки:")
            for col in results['columns']:
                print(f">{col['column_name']} в таблице {col['table_name']} (источник: {col['source_name']})")
        
        print()
    
    def print_schema(self, schema: Dict[str, Any]):
        """Выводит схему таблицы"""
        if not schema:
            print("Таблица не найдена")
            return
        
        print(f"Схема таблицы: {schema['table_name']}")
        print(f"Источник: {schema['source_name']}")
        print(f"Колонки ({len(schema['columns'])}):")
        for col in schema['columns']:
            print(f">{col}")
        
        if schema['sample_data']:
            print(f"Пример данных (первые {len(schema['sample_data'])} строк):")
            for i, row in enumerate(schema['sample_data'], 1):
                print(f"Строка {i}:")
                for key, value in row.items():
                    print(f"    {key}: {value}")
        print()
    
    def run(self):
        """Запускает CLI"""
        self.print_help()
        
        while True:
            try:
                user_input = input("Ввод > ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("До свидания!")
                    break
                
                elif user_input.lower() == 'help':
                    self.print_help()
                
                elif user_input.lower() == 'list':
                    sources = self.mcp_tools.list_sources()
                    if sources:
                        print("Источники данных:")
                        for src in sources:
                            print(f">{src['source_id']}: {src['name']}")
                    else:
                        print("Нет настроенных источников данных")
                
                elif user_input.startswith('index '):
                    parts = user_input.split()
                    if len(parts) == 2:
                        source_id = parts[1]
                        result = self.mcp_tools.index_source(source_id)
                        if result['success']:
                            print(f"{result['message']}")
                        else:
                            print(f"{result['message']}")
                    else:
                        print("Использование: index <source_id>")
                
                elif user_input.startswith('search '):
                    query = user_input[7:].strip()
                    if query:
                        results = self.mcp_tools.search(query)
                        self.print_search_results(results)
                    else:
                        print("Введите поисковый запрос")
                
                elif user_input.startswith('schema '):
                    parts = user_input.split()
                    if len(parts) == 3:
                        source_id, table_name = parts[1], parts[2]
                        schema = self.mcp_tools.get_schema(source_id, table_name)
                        self.print_schema(schema)
                    else:
                        print("Использование: schema <source_id> <table_name>")
                
                else:
                    print("Неизвестная команда. Введите 'help' для справки.")
            
            except KeyboardInterrupt:
                print("До свидания!")
                break
            except Exception as e:
                print(f"Ошибка: {e}")