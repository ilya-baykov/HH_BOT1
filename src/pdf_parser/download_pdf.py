import os
from requests import Response

from config.constants.paths import RESUMES_ROOT_PATH
from config.logger import logger


class PDFDownloader:
    def __init__(self, recruiter_surname: str, vacancy_id: str, candidate_surname: str):
        """
        Инициализация класса для скачивания резюме по сформированному пути
        :param recruiter_surname: Фамилия рекрутера, используется для создания директории.
        :param vacancy_id: Идентификатор вакансии, используется для создания директории.
        :param candidate_surname: Фамилия кандидата, используется для создания директории.
        """
        self._recruiter_surname = recruiter_surname.strip()
        self._vacancy_id = vacancy_id.strip()
        self._candidate_surname = candidate_surname.strip()
        self._folder_path = self._create_folders()
        self._resume_pdf_path = os.path.join(self.folder_path, 'resume.pdf')  # Путь для сохранения резюме

    def _create_folders(self) -> str:
        """Создаёт папки для сохранения резюме"""
        try:
            recruiter_dir = os.path.join(RESUMES_ROOT_PATH,
                                         self._recruiter_surname.strip())  # папка с фамилией рекрутера
            vacancy_dir = os.path.join(recruiter_dir, self._vacancy_id.strip())  # Создаем папку с номером вакансии
            candidate_dir = os.path.join(vacancy_dir, self._candidate_surname)  # Создаем папку с фамилией соискателя

            os.makedirs(candidate_dir, exist_ok=True)  # Создаем все необходимые папки, если они не существуют
            return candidate_dir
        except Exception as e:
            logger.error(f"При попытке создать папки для сохранения резюме - произошла ошибка:{e}")

    def download(self, download_response: Response):
        """
        Скачивает файл резюме и сохраняет его в соответствующую директорию.

        :param download_response: Ответ от запроса, содержащий файл резюме.

        """

        try:
            # Сохраняем файл
            with open(self._resume_pdf_path, 'wb') as f:
                f.write(download_response.content)

            logger.info(f"Файл резюме успешно сохранен: {self._resume_pdf_path}")

        except Exception as e:
            logger.error(f"Ошибка при скачивании файла резюме: {e}")

    @property
    def resume_pdf_path(self):
        """Возвращает путь к пдф-резюме"""
        return self._resume_pdf_path

    @property
    def folder_path(self):
        """Возвращает путь к папке с резюме"""
        return self._folder_path
