from typing import Dict, Any, List, Optional

from database.database import Database
from logger import logger


class DatabaseOperations:
    @staticmethod
    def insert_data(table_name: str, data: Dict[str, Any]) -> None:
        """Вставка данных в указанную таблицу."""
        db = Database()
        db.connect()
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            db.cursor.execute(query, tuple(data.values()))
            db.conn.commit()
            logger.info(f"Данные успешно вставлены в таблицу {table_name}.")
        except Exception as e:
            logger.error(f"Ошибка вставки данных в таблицу {table_name}: {e}")
        finally:
            db.close()

    @staticmethod
    def fetch_data(table_name: str, column_name: str, value: Any) -> Optional[List[Dict[str, Any]]]:
        """Считывание данных из указанной таблицы по заданному полю."""
        db = Database()
        db.connect()
        try:
            query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
            db.cursor.execute(query, (value,))
            results = db.cursor.fetchall()
            logger.info(f"Данные успешно считаны из таблицы {table_name}.")
            return results
        except Exception as e:
            logger.error(f"Ошибка считывания данных из таблицы {table_name}: {e}")
            return None
        finally:
            db.close()


db_operations = DatabaseOperations()
