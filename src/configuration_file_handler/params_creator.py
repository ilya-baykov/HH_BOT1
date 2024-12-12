from typing import Any

from src.configuration_file_handler.enums_for_dataclass import Relocation, Field, Logic, Period
from src.configuration_file_handler.file_dataclass import RecruiterDataParams
from config.logger import logger


class ParamsCollector:
    def __init__(self, recruiter_params: RecruiterDataParams):
        self.recruiter_params = recruiter_params

    @property
    def get_params(self) -> dict[str, Any]:
        params = {
            'per_page': 15,  # Количество резюме на странице
            'salary_from': self.recruiter_params.salary_range.salary_from,  # Минимальная зарплата
            'salary_to': self.recruiter_params.salary_range.salary_to,  # Максимальная зарплата
            'age_from': self.recruiter_params.age_range.age_from,  # Минимальный возраст
            'age_to': self.recruiter_params.age_range.age_to,  # Максимальный возраст
            'area': self.recruiter_params.search_territory,  # Регион поиска
            'relocation': Relocation.LIVING.value,  # Готовность к переезду
            'gender': self.recruiter_params.gender,  # Пол соискателя
            'job_search_status': self.recruiter_params.job_search_status,  # Статус поиска работы
            'employment': self.recruiter_params.employment,  # Тип занятости
            'experience': self.recruiter_params.experience,  # Опыт работы
            'schedule': self.recruiter_params.schedule,  # График работы
            'label': self.recruiter_params.label,  # Дополнительный фильтр
            'skill': self.recruiter_params.skills,  # id Ключевых умений
            'citizenship': '113',  # Гражданство (Россия)
        }
        # Удаляем пары, где значения равны None
        params = {key: value for key, value in params.items() if value is not None}

        logger.info(f"Параметры для поиска:{params}")

        return params

    @property
    def get_text_search(self) -> str:
        text_params = self.recruiter_params.generate_text_params(phrases_list=self.recruiter_params.vacancy,
                                                                 logic=Logic.ANY, field=Field.EVERYWHERE,
                                                                 period=Period.LAST_YEAR)
        logger.info(f"Текст для поиска подходящих вакансий :{text_params}")

        return text_params
