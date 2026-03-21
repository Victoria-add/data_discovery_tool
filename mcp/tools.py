from typing import Dict, List, Any, Optional
from index import MetadataIndex
from search import SearchEngine

class MCPTools:
    """MCP инструменты для AI-агента"""
    
    def __init__(self, metadata_index: MetadataIndex, search_engine: SearchEngine):
        self.metadata_index = metadata_index
        self.search_engine = search_engine
    
    def list_sources(self) -> List[Dict[str, str]]:
        """
        Возвращает список всех источников данных
        """
        return self.metadata_index.list_sources()
    
    def index_source(self, source_id: str) -> Dict[str, Any]:
        """
        Индексирует указанный источник данных
        """
        success = self.metadata_index.index_source(source_id)
        return {
            'success': success,
            'source_id': source_id,
            'message': f"Source {source_id} indexed successfully" if success else f"Failed to index source {source_id}"
        }
    
    def search(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Выполняет поиск по ключевому слову
        """
        return self.search_engine.search(query)
    
    def get_schema(self, source_id: str, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Получает схему таблицы с примером данных
        """
        return self.search_engine.get_table_schema(source_id, table_name)