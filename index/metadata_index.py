from typing import Dict, List, Any, Optional
from connectors.base import DataConnector

class MetadataIndex:
    """Индекс метаданных для поиска"""
    
    def __init__(self):
        self.sources: Dict[str, DataConnector] = {}
        self.index: Dict[str, List[Dict[str, Any]]] = {
            'tables': [],
            'columns': []
        }
    
    def add_source(self, source_id: str, connector: DataConnector) -> None:
        """Добавляет источник данных"""
        self.sources[source_id] = connector
    
    def index_source(self, source_id: str) -> bool:
        """Индексирует источник данных"""
        if source_id not in self.sources:
            return False
        
        connector = self.sources[source_id]
        
        try:
            schema = connector.get_schema()
            
            for table_name, columns in schema.items():
                # Индексируем таблицу
                self.index['tables'].append({
                    'source_id': source_id,
                    'source_name': connector.name,
                    'table_name': table_name,
                    'type': 'table'
                })
                
                # Индексируем колонки
                for column in columns:
                    self.index['columns'].append({
                        'source_id': source_id,
                        'source_name': connector.name,
                        'table_name': table_name,
                        'column_name': column,
                        'type': 'column'
                    })
            
            return True
            
        except Exception as e:
            print(f"Ошибка при индексации {source_id}: {e}")
            return False
    
    def search(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """Поиск по индексу"""
        query_lower = query.lower()
        results = {
            'tables': [],
            'columns': []
        }
        
        # Поиск по таблицам
        for table in self.index['tables']:
            if query_lower in table['table_name'].lower():
                results['tables'].append(table)
        
        # Поиск по колонкам
        for column in self.index['columns']:
            if query_lower in column['column_name'].lower():
                results['columns'].append(column)
        
        return results
    
    def get_schema(self, source_id: str, table_name: str) -> Optional[Dict[str, Any]]:
        """Получает схему таблицы с примером данных"""
        if source_id not in self.sources:
            return None
        
        connector = self.sources[source_id]
        
        try:
            schema = connector.get_schema()
            if table_name not in schema:
                return None
            
            sample_data = connector.get_sample_data(table_name, 5)
            
            return {
                'source_id': source_id,
                'source_name': connector.name,
                'table_name': table_name,
                'columns': schema[table_name],
                'sample_data': sample_data
            }
            
        except Exception as e:
            print(f"Ошибка при получении схемы {source_id}/{table_name}: {e}")
            return None
    
    def list_sources(self) -> List[Dict[str, str]]:
        """Возвращает список источников данных"""
        return [
            {'source_id': sid, 'name': connector.name}
            for sid, connector in self.sources.items()
        ]