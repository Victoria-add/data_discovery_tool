from typing import Dict, List, Any
from index import MetadataIndex

class SearchEngine:
    """Поисковый движок"""
    
    def __init__(self, metadata_index: MetadataIndex):
        self.metadata_index = metadata_index
    
    def search(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """Выполняет поиск по запросу"""
        if not query or not query.strip():
            return {'tables': [], 'columns': []}
        
        return self.metadata_index.search(query)
    
    def get_table_schema(self, source_id: str, table_name: str) -> Dict[str, Any]:
        """Получает схему таблицы"""
        return self.metadata_index.get_schema(source_id, table_name)