from abc import ABC, abstractmethod
from typing import Dict, List, Any

class DataConnector(ABC):
    """Базовый класс для всех коннекторов к источникам данных"""
    def __init__(self, source_id: str, name: str):
        self.source_id = source_id
        self.name = name
    
    @abstractmethod
    def get_schema(self) -> Dict[str, List[str]]:
        """Возвращает схему данных: """
        pass
    
    @abstractmethod
    def get_sample_data(self, table: str, limit: int) -> List[Dict[str, Any]]:
        """Возвращает пример данных из таблицы"""
        pass
    
    @abstractmethod
    def get_all_tables(self) -> List[str]:
        """Возвращает список всех таблиц"""
        pass