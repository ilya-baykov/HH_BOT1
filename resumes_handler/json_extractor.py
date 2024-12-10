import re
import json
from logger import logger


class JsonExtractor:
    @staticmethod
    def extract_json(data_str):
        """
        Извлекает JSON из строки.

        :param data_str: Исходная строка, содержащая JSON.
        :return: Словарь с данными JSON или None, если JSON не найден.
        """

        # Используем регулярное выражение для извлечения текста внутри фигурных скобок
        match = re.search(r'\{.*\}', data_str, re.DOTALL)
        if match:
            json_str = match.group(0)  # Получаем текст внутри фигурных скобок
            try:
                # Преобразуем строку в JSON
                return json.loads(json_str)
            except json.JSONDecodeError:
                logger.error("Ошибка декодирования JSON.")
            except Exception as e:
                logger.error(f"При попытке преобразовать ответ нейросети в json - произошла ошибка: {e}")
        else:
            logger.warning("JSON не найден.")
