from typing import Dict, Any, List, Optional

import pandas as pd

from src.database.database import Database
from config.logger import logger


class DatabaseOperations:
    @staticmethod
    def insert_data_from_dataframe(db: Database, table_name: str, data: pd.DataFrame, auto_close: bool) -> None:
        """Вставка данных из DataFrame в указанную таблицу."""
        try:
            # Получаем имена столбцов и значения
            columns = ', '.join(data.columns)
            placeholders = ', '.join(['%s'] * len(data.columns))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Подготовка данных для пакетной вставки
            data_to_insert = [tuple(row) for row in data.values]

            # Выполнение пакетной вставки
            db.cursor.executemany(query, data_to_insert)

            db.conn.commit()
            logger.info(f"Данные успешно вставлены в таблицу {table_name}.")
        except Exception as e:
            logger.error(f"Ошибка вставки данных в таблицу {table_name}: {e}")
        finally:
            if auto_close:
                db.close()

    @staticmethod
    def fetch_data(db: Database, table_name: str, column_name: str, value: Any,
                   auto_close: bool) -> Optional[List[Dict[str, Any]]]:
        """Считывание данных из указанной таблицы по заданному полю."""
        try:
            query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
            db.cursor.execute(query, (value,))
            results = db.cursor.fetchall()
            logger.debug(f"Данные успешно считаны из таблицы {table_name}.")
            return results
        except Exception as e:
            logger.error(f"Ошибка считывания данных из таблицы {table_name}: {e}")
            return None
        finally:
            if auto_close:
                db.close()


db_operations = DatabaseOperations()
