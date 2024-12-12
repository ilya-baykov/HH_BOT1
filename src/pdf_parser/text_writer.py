from config.logger import logger


class TextWriter:
    """Класс для создания текстового файла"""

    @staticmethod
    def write_pdf(file_path: str, content: str):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Файл '{file_path}' успешно записан.")
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}. Проверьте путь.")
        except PermissionError:
            logger.error(f"Нет прав для записи в файл: {file_path}.")
        except Exception as e:
            logger.error(f"Произошла ошибка при записи в файл '{file_path}': {e}")
