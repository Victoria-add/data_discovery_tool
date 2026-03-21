import sqlite3
from typing import Dict, List, Any
from .base import DataConnector

class SQLiteConnector(DataConnector):
    """Коннектор для SQLite базы данных"""
    
    def __init__(self, source_id: str, name: str, db_path: str):
        super().__init__(source_id, name)
        self.db_path = db_path
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_all_tables(self) -> List[str]:
        """Получает все таблицы из базы"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    
    def get_schema(self) -> Dict[str, List[str]]:
        """Получает схему всех таблиц"""
        schema = {}
        tables = self.get_all_tables()
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            schema[table] = columns
        
        conn.close()
        return schema
    
    def get_sample_data(self, table: str, limit: int) -> List[Dict[str, Any]]:
        """Получает пример данных из таблицы"""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"SELECT * FROM '{table}' LIMIT ?", (limit,))
            rows = [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении данных из {table}: {e}")
            rows = []
        
        conn.close()
        return rows