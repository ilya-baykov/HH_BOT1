import os
import psycopg2

from config.logger import logger


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Подключение к базе данных."""
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            self.cursor = self.conn.cursor()
            logger.info("Подключение к базе данных успешно.")
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("Соединение с базой данных закрыто.")


report_database = Database()
