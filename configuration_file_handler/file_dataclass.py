from dataclasses import dataclass
from typing import List, Optional

from requests import Response

from configuration_file_handler.enums_for_dataclass import *
from requests_handler.requests_manager import request_manager
from logger import logger


@dataclass
class RecruiterDataParams:
    fio_recruiter: str  # ФИО рекрутера (полностью)
    email_recruiter: str  # Почта рекрутера
    application_number: str  # Номер заявки в IQHR/ссылка на заявку
    vacancy: str  # Вакансия по штатной книге

    region: str  # Регион (территория поиска)
    city: str  # Город (место трудоустройства)

    job_title: str  # Название должности (ключевые слова или варианты поиска)
    main_responsibilities: str  # Основные обязанности (ключевые слова)

    education: Optional[str]  # Образование (минимальный уровень)

    search_status: Optional[str]  # Статус поиска

    additional_education: Optional[str]  # Дополнительное образование (Наличие сертификатов, лицензий)

    required_experience: str  # Необходимый опыт работы (отрасль, должности, уровень ответственности и др.)

    employment_type_full_time: str | BinaryChoice  # Тип занятости: Полная занятость
    employment_type_part_time: str | BinaryChoice  # Тип занятости: Частичная занятость
    employment_type_project: str | BinaryChoice  # Тип занятости: Проектная работа/разовое задание
    employment_type_internship: str | BinaryChoice  # Тип занятости: Стажировка
    work_schedule_full_day: str | BinaryChoice  # График работы: Полный день
    work_schedule_shift: str | BinaryChoice  # График работы: Сменный график
    work_schedule_flexible: str | BinaryChoice  # График работы: Гибкий график
    work_schedule_remote: str | BinaryChoice  # График работы: Удаленная работа
    work_schedule_rotational: str | BinaryChoice  # График работы: Вахтовый метод

    salary: str  # Заработная плата

    age: str  # Возраст

    gender_preference: Optional[Gender]  # Пол (предпочтения руководителя)

    citizenship: str  # Гражданство (всегда указывается Россия)

    work_experience: str  # Стаж работы (с опытом/без опыта)

    software_knowledge: str  # Знание/владение ПО (ключевые требования к владению ПО)

    specialization: Optional[str]  # Специализация (указать из справочника специализации, если не требуется - None)

    show_resume_without_salary: str | BinaryChoice  # Показывать резюме без указания зарплаты

    resume_view_depth: str  # Глубина просмотра резюме на HH.ru в днях

    exclude_resume_keywords: str | BinaryChoice  # Требуется ли исключить резюме из поиска по ключевым словам
    exclude_keywords: Optional[str]  # Слова, с которыми робот не должен искать резюме
    exclude_resume_phrases: Optional[str | ExclusionCriteria]  # Исключать резюме, в которых содержатся
    exclude_keywords_in: List[str]  # Ключевые слова для исключения содержатся
    exclude_in_everywhere: Optional[str | BinaryChoice]  # Везде
    exclude_in_resume_title: Optional[str | BinaryChoice]  # В названии резюме
    exclude_in_education: Optional[str | BinaryChoice]  # В образовании
    exclude_in_skills: Optional[str | BinaryChoice]  # В ключевых навыках
    exclude_in_work_experience: Optional[str | BinaryChoice]  # В опыте работы

    @property
    def search_territory(self) -> list[str]:
        """Возвращает регионы для поиска в виде списка area_id"""
        regions: list[str] = self.region.split(",")  # Список регионов из настроечного файла
        areas_ids = set()  # множество для хранения уникальных area_id регионов

        for region in regions:
            area_response: Response = request_manager.reference_book_get.get_areas(text=region)  # Запрос к API
            try:

                items: list[dict] = area_response.json().get('items')
                if items:
                    items_ids = [item.get('id') for item in items]
                    logger.debug(f"Для региона={region} были получены такие id:[{items_ids}]")
                    areas_ids.update(items_ids)
                else:
                    logger.error(f"Для региона={region} не получилось получить items]")

            except Exception as e:
                logger.error(f"При попытке получить id регионов-произошла ошибка - {e}")

        unique_ids: list[str] = list(set(areas_ids))  # Убираем дубликаты
        return unique_ids

    @staticmethod
    def generate_text_params(phrases_list: str,
                             logic: Logic = Logic.ANY,
                             field: Field = Field.EVERYWHERE,
                             period: Period = Period.LAST_YEAR) -> str:
        """
           Формирует текстовый параметр на основе переданного списка фраз.

           Параметры:
           ----------
           phrases_list : str
               Строка, содержащая фразы, разделенные запятыми. Каждая фраза будет обработана для формирования
               поискового запроса.

           Logic : str, по умолчанию 'any'
               Логика поиска, определяющая, как обрабатываются фразы:
               - 'all': Все слова должны встречаться.
               - 'any': Любое из слов должно встречаться.
               - 'phrase': Должна встречаться точная фраза.
               - 'except': Указывает, что слова не должны встречаться.

           Field : str, по умолчанию 'everywhere'
               Поле, в котором будет производиться поиск. Возможные значения:
               - 'everywhere': Поиск по всем полям.
               - 'title': Поиск в названии резюме.
               - 'education': Поиск в образовании.
               - 'skills': Поиск в ключевых навыках.
               - 'experience': Поиск в опыте работы.
               - 'experience_company': Поиск в компаниях и отраслях.
               - 'experience_position': Поиск в должностях.
               - 'experience_description': Поиск в обязанностях.

           Period : str, по умолчанию 'last_year'
               Период, за который будет производиться поиск. Например, 'last_year' для поиска за последний год.
        """

        # Получаем список поисковых словосочетаний для фильтрации
        search_phrases = [f'"{phrases.strip()}"' for phrases in phrases_list.split(',') if phrases.strip()]

        # Формируем строку с текстовыми параметрами для логического ИЛИ
        text_params = (f"text={' OR '.join(search_phrases)}&text.logic={logic.value}&"
                       f"text.field={field.value}&"
                       f"text.period={period.value}")

        logger.debug(f"Для поиска были сформированы такие параметры: {text_params}")
        return text_params
