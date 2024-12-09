import math
import re
from dataclasses import dataclass
from typing import List, Optional

from requests import Response

from configuration_file_handler.enums_for_dataclass import *
from configuration_file_handler.exeptions import MissingParameterError
from configuration_file_handler.literals import *
from requests_handler.requests_manager import request_manager
from logger import logger


@dataclass
class RecruiterDataParams:
    fio_recruiter: str  # ФИО рекрутера (полностью)
    email_recruiter: str  # Почта рекрутера
    application_number: str  # Номер заявки в IQHR/ссылка на заявку
    vacancy: str  # Вакансия по штатной книге

    region: str  # Регион (территория поиска)
    city: Optional[str]  # Город (место трудоустройства)

    job_title: str  # Название должности (ключевые слова или варианты поиска)
    main_responsibilities: str  # Основные обязанности (ключевые слова)

    education: EducationLevelLiteral  # Образование (минимальный уровень)

    search_status: Optional[str]  # Статус поиска

    additional_education: Optional[str]  # Дополнительное образование (Наличие сертификатов, лицензий)

    required_experience: str  # Необходимый опыт работы (отрасль, должности, уровень ответственности и др.)

    employment_type_full_time: BinaryChoiceLiteral  # Тип занятости: Полная занятость
    employment_type_part_time: BinaryChoiceLiteral  # Тип занятости: Частичная занятость
    employment_type_project: BinaryChoiceLiteral  # Тип занятости: Проектная работа/разовое задание
    employment_type_internship: BinaryChoiceLiteral  # Тип занятости: Стажировка
    work_schedule_full_day: BinaryChoiceLiteral  # График работы: Полный день
    work_schedule_shift: BinaryChoiceLiteral  # График работы: Сменный график
    work_schedule_flexible: BinaryChoiceLiteral  # График работы: Гибкий график
    work_schedule_remote: BinaryChoiceLiteral  # График работы: Удаленная работа
    work_schedule_rotational: BinaryChoiceLiteral  # График работы: Вахтовый метод

    salary: str  # Заработная плата

    age: str  # Возраст

    gender_preference: Optional[GenderLiteral]  # Пол (предпочтения руководителя)

    citizenship: str  # Гражданство (всегда указывается Россия)

    work_experience: str  # Стаж работы (с опытом/без опыта)

    software_knowledge: str  # Знание/владение ПО (ключевые требования к владению ПО)

    specialization: Optional[str]  # Специализация (указать из справочника специализации, если не требуется - None)

    show_resume_without_salary: BinaryChoiceLiteral  # Показывать резюме без указания зарплаты

    resume_view_depth: str  # Глубина просмотра резюме на HH.ru в днях

    exclude_resume_keywords: BinaryChoiceLiteral  # Требуется ли исключить резюме из поиска по ключевым словам
    exclude_keywords: Optional[str]  # Слова, с которыми робот не должен искать резюме
    exclude_resume_phrases: Optional[ExclusionCriteriaLiteral]  # Исключать резюме, в которых содержатся
    exclude_keywords_in: List[str]  # Ключевые слова для исключения содержатся
    exclude_in_everywhere: Optional[BinaryChoiceLiteral]  # Везде
    exclude_in_resume_title: Optional[BinaryChoiceLiteral]  # В названии резюме
    exclude_in_education: Optional[BinaryChoiceLiteral]  # В образовании
    exclude_in_skills: Optional[BinaryChoiceLiteral]  # В ключевых навыках
    exclude_in_work_experience: Optional[BinaryChoiceLiteral]  # В опыте работы

    def __post_init__(self):
        # Проверка обязательных параметров
        if not self.fio_recruiter:
            raise MissingParameterError("ФИО рекрутера обязательно.")
        if not self.email_recruiter:
            raise MissingParameterError("Почта рекрутера обязательна.")
        if not self.application_number:
            raise MissingParameterError("Номер заявки обязателен.")
        if not self.vacancy:
            raise MissingParameterError("Вакансия обязательна.")
        if not self.region:
            raise MissingParameterError("Регион обязателен.")
        if not self.job_title:
            raise MissingParameterError("Название должности обязательно.")
        if not self.main_responsibilities:
            raise MissingParameterError("Основные обязанности обязательны.")
        if not self.education:
            raise MissingParameterError("Минимальный уровень образования обязателен")
        if not self.required_experience:
            raise MissingParameterError("Необходимый опыт работы обязателен.")
        if not self.salary:
            raise MissingParameterError("Заработная плата обязательна.")
        if not self.age:
            raise MissingParameterError("Возраст обязателен")

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

        unique_ids: list[str] = list(areas_ids)  # Убираем дубликаты
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

    @property
    def education_level(self) -> Optional[str]:
        education_mapping = {
            'Среднее': EducationLevel.SECONDARY.value,
            'Среднее специальное': EducationLevel.SPECIAL_SECONDARY.value,
            'Незаконченное высшее': EducationLevel.UNFINISHED_HIGHER.value,
            'Бакалавр': EducationLevel.BACHELOR.value,
            'Магистр': EducationLevel.MASTER.value,
            'Высшее': EducationLevel.HIGHER.value
        }

        education_id = education_mapping.get(self.education)
        return education_id

    @property
    def salary_range(self) -> SalaryRange:
        """
        Парсит строку с диапазоном зарплаты и возвращает именованный кортеж.

        :return: Именованный кортеж с полями salary_from и salary_to.
        """
        pattern = r'от\s*(\d+)\s*до\s*(\d+)'  # Шаблон для поиска диапазона: "от <число> до <число>", игнорируя пробелы.
        match = re.search(pattern, self.salary)
        if match:
            salary_from = int(match.group(1))
            salary_to = int(match.group(2))
            return SalaryRange(salary_from=salary_from, salary_to=salary_to)
        else:
            logger.error(f"Не удалось распарсить строку зарплаты: {self.salary}")

    @property
    def age_range(self) -> AgeRange:
        """
        Парсит строку с диапазоном возраста и возвращает именованный кортеж.

        :return: Именованный кортеж с полями age_from и age_to.
        """
        pattern = r'от\s*(\d+)\s*до\s*(\d+)'  # Шаблон для поиска диапазона: "от <число> до <число>", игнорируя пробелы.

        match = re.search(pattern, self.age)
        if match:
            age_from = int(match.group(1))
            age_to = int(match.group(2))
            return AgeRange(age_from=age_from, age_to=age_to)
        else:
            logger.error(f"Не удалось распарсить строку возраста: {self.age}")

    @property
    def gender(self) -> Optional[str]:
        """Возвращает идентификатор пола на основе предпочтения пола из настроечного файла."""
        gender_map = {
            'Мужской': Gender.MALE.value,
            'Женский': Gender.FEMALE.value,
            'Любой': Gender.ANY.value
        }
        if self.gender_preference:
            return gender_map.get(self.gender_preference)

    @property
    def job_search_status(self) -> Optional[str]:
        """Возвращает идентификатор статуса поиска работы на основе предпочтения."""
        status_mapping = {
            'Активно ищет работу': JobSearchStatusEnum.ACTIVE_SEARCH.value,
            'Рассматривает предложения': JobSearchStatusEnum.LOOKING_FOR_OFFERS.value,
            'Не ищет работу': JobSearchStatusEnum.NOT_LOOKING_FOR_JOB.value,
            'Предложили работу, решает': JobSearchStatusEnum.HAS_JOB_OFFER.value,
            'Вышел на новое место': JobSearchStatusEnum.ACCEPTED_JOB_OFFER.value,
        }
        return status_mapping.get(self.search_status)

    @property
    def employment(self) -> Optional[str]:
        """Возвращает тип занятости employment """
        if self.employment_type_full_time.lower() == "да":  # # 'Полная занятость'
            return EmploymentType.FULL.value
        elif self.employment_type_part_time.lower() == "да":  # 'Частичная занятость'
            return EmploymentType.PART.value
        elif self.employment_type_project.lower() == "да":  # 'Проектная работа'
            return EmploymentType.PROJECT.value
        elif self.employment_type_internship.lower() == "да":  # 'Стажировка'
            return EmploymentType.PROBATION.value

    @property
    def schedule(self) -> Optional[str]:
        """Возвращает график работы schedule """
        if self.work_schedule_full_day:  # График работы: Полный день
            return WorkSchedule.FULL_DAY.value
        if self.work_schedule_shift:  # График работы: Сменный график
            return WorkSchedule.SHIFT.value
        if self.work_schedule_flexible:  # График работы: Гибкий график
            return WorkSchedule.FLEXIBLE.value
        if self.work_schedule_remote:  # График работы: Удаленная работа
            return WorkSchedule.REMOTE.value
        if self.work_schedule_rotational:  # График работы: Вахтовый метод
            return WorkSchedule.FLY_IN_FLY_OUT.value

    @property
    def experience(self) -> Optional[str]:
        """Возвращает стаж работы для фильтрации поиска резюме"""
        experience_mapping = {
            'Нет опыта': ExperienceType.NO_EXPERIENCE.value,
            'От 1 года до 3 лет': ExperienceType.BETWEEN_1_AND_3.value,
            'От 3 до 6 лет': ExperienceType.BETWEEN_3_AND_6.value,
            'Более 6 лет': ExperienceType.MORE_THAN_6.value,
        }
        return experience_mapping.get(self.work_experience)

    @property
    def label(self) -> Optional[str]:
        if self.show_resume_without_salary and self.show_resume_without_salary.lower() == "да":
            return LabelType.ONLY_WITH_SALARY.value

    @property
    def skills(self) -> Optional[list[str]]:

        if self.specialization is None or (isinstance(self.specialization, float) and math.isnan(self.specialization)):
            return None

        skills_ids = set()
        specializations = self.specialization.split(',')
        for specialization in specializations:
            skill_set_response: Response = request_manager.reference_book_get.get_skill_set(specialization)

            try:
                items: list[dict] = skill_set_response.json().get('items')
                if items:
                    items_ids = [item.get('id') for item in items]
                    logger.debug(f"Для специализации={specialization} были получены такие id:[{items_ids}]")
                    skills_ids.update(items_ids)
                else:
                    logger.error(f"Для специализации={specialization} не получилось получить items]")
            except Exception as e:
                logger.error(f"При попытке получить id специализации-произошла ошибка - {e}")

        unique_ids: list[str] = list(skills_ids)  # Убираем дубликаты
        return unique_ids
