import csv
import os
from typing import Dict, List, Any
from .base import DataConnector

class CSVConnector(DataConnector):
    """Коннектор для CSV файлов"""
    
    def __init__(self, source_id: str, name: str, folder_path: str):
        super().__init__(source_id, name)
        self.folder_path = folder_path
    
    def get_all_tables(self) -> List[str]:
        """Получает все CSV файлы в папке"""
        csv_files = []
        if os.path.exists(self.folder_path):
            for file in os.listdir(self.folder_path):
                if file.endswith('.csv'):
                    csv_files.append(file[:-4])
        return csv_files
    
    def _read_csv(self, table: str) -> List[Dict[str, Any]]:
        """Читает CSV файл и возвращает список словарей"""
        file_path = os.path.join(self.folder_path, f"{table}.csv")
        data = []
        
        if not os.path.exists(file_path):
            return data
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data
    
    def get_schema(self) -> Dict[str, List[str]]:
        """Получает схему всех CSV файлов"""
        schema = {}
        tables = self.get_all_tables()
        
        for table in tables:
            data = self._read_csv(table)
            if data and len(data) > 0:
                schema[table] = list(data[0].keys())
            else:
                schema[table] = []
        
        return schema
    
    def get_sample_data(self, table: str, limit: int) -> List[Dict[str, Any]]:
        """Получает пример данных из CSV"""
        data = self._read_csv(table)
        return data[:limit]