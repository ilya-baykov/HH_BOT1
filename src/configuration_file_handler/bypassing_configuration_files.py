import os

from src.configuration_file_handler.file_dataclass import RecruiterDataParams
from src.configuration_file_handler.read_file import RecruiterDataReader
from config.constants.paths import CONFIGURATION_FILES_PATH


class ConfigurationFilesHandler:
    """Класс для работы с настроечными файлами"""

    def __init__(self, configuration_file_path: str = CONFIGURATION_FILES_PATH):
        """
        Инициализация
        :param configuration_file_path: Корневой путь к папке с настроечными файлами
        """
        self.configuration_file_path = configuration_file_path
        self._configuration_files: list = [f for f in os.listdir(self.configuration_file_path) if f.endswith('.xlsx')]

    def bypassing_files(self):
        for file_name in self._configuration_files:
            file_path = os.path.join(self.configuration_file_path, file_name)
            recruiter_params: RecruiterDataParams = RecruiterDataReader(file_path=file_path).read_data()
            yield recruiter_params
