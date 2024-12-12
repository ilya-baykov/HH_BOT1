import os

from dotenv import load_dotenv

from config.constants.paths import ENV_PATH
from exeptions import EnvFileLoadError
from config.logger import logger


class EnvLoader:
    """Класс для работы с переменными окружения"""

    def __init__(self, env_dir: str = ENV_PATH):
        """
        Инициализация класса EnvLoader.

        :param env_dir: Путь к директории, содержащей .env файлы.
        """
        self._env_dir = env_dir
        self._env_paths = self._get_env_files()

    def _get_env_files(self) -> list[str]:
        """Получение списка всех .env файлов в указанной директории."""
        env_files = []
        for file in os.listdir(self._env_dir):
            if file.startswith('.env'):  # Проверяем, начинается ли имя файла с .env
                env_files.append(os.path.join(self._env_dir, file))
        return env_files

    def load_env_files(self) -> None:
        """Загрузка всех .env файлов из списка."""
        for path in self._env_paths:
            if os.path.exists(path):
                try:
                    load_dotenv(dotenv_path=path)
                    logger.info(f"Файл {path} успешно загружен.")
                except Exception as e:
                    logger.error(f"При попытке загрузить файл: {path} произошла ошибка - {e}")
                    raise EnvFileLoadError(f"Не удалось загрузить файл: {path}") from e
            else:
                logger.warning(f"Файл {path} не найден. Переменные окружения не загружены.")


EnvLoader().load_env_files()  # Загружаем все переменные окружения
