from enum import Enum
from typing import NamedTuple


class Logic(Enum):
    """
    Перечисление для логики поиска.

    Используется в методе `generate_text_params` для определения,
    как обрабатываются фразы в поисковом запросе.
    """
    ALL = 'all'  # Все слова должны встречаться.
    ANY = 'any'  # Любое из слов должно встречаться.
    PHRASE = 'phrase'  # Должна встречаться точная фраза.
    EXCEPT = 'except'  # Указывает, что слова не должны встречаться.


class Field(Enum):
    """
    Перечисление для полей поиска.

    Используется в методе `generate_text_params` для указания,
    в каком поле будет производиться поиск.
    """
    EVERYWHERE = 'everywhere'  # Поиск по всем полям.
    TITLE = 'title'  # Поиск в названии резюме.
    EDUCATION = 'education'  # Поиск в образовании.
    SKILLS = 'skills'  # Поиск в ключевых навыках.
    EXPERIENCE = 'experience'  # Поиск в опыте работы.
    EXPERIENCE_COMPANY = 'experience_company'  # Поиск в компаниях и отраслях.
    EXPERIENCE_POSITION = 'experience_position'  # Поиск в должностях.
    EXPERIENCE_DESCRIPTION = 'experience_description'  # Поиск в обязанностях.


class Period(Enum):
    """
    Перечисление для периодов поиска.

    Используется в методе `generate_text_params` для указания,
    за какой период будет производиться поиск.
    """
    LAST_YEAR = 'last_year'  # Поиск за последний год.
    LAST_MONTH = 'last_month'  # Поиск за последний месяц.
    LAST_WEEK = 'last_week'  # Поиск за последнюю неделю.
    ALL_TIME = 'all_time'  # Поиск за все время.


class Relocation(Enum):
    """
    Перечисление для периодов поиска.

    Готовность к переезду. Возможные значения указаны в поле resume_search_relocation в справочнике полей.
    Необходимо указывать вместе с параметром area
    """
    LIVING_OR_RELOCATION = 'living_or_relocation'  # Живут в указанном регионе или готовы переехать в него
    LIVING = 'living'  # Живут в указанном регионе
    LIVING_BUT_RELOCATION = 'living_but_relocation'  # Живут в указанном регионе и готовы к переезду куда-либо
    RELOCATION = 'relocation'  # Не живут в указанном регионе, но готовы переехать в него


class JobSearchStatusEnum(Enum):
    """Используется для получения job_search_status в фильтрации поиска резюме"""
    ACTIVE_SEARCH = "active_search"  # 'Активно ищет работу'
    LOOKING_FOR_OFFERS = 'looking_for_offers'  # 'Рассматривает предложения'
    NOT_LOOKING_FOR_JOB = 'not_looking_for_job'  # 'Не ищет работу'
    HAS_JOB_OFFER = 'has_job_offer'  # 'Предложили работу, решает'
    ACCEPTED_JOB_OFFER = 'accepted_job_offer'  # 'Вышел на новое место'


class ExperienceType(Enum):
    NO_EXPERIENCE = 'noExperience'  # 'Нет опыта'
    BETWEEN_1_AND_3 = 'between1And3'  # 'От 1 года до 3 лет'
    BETWEEN_3_AND_6 = 'between3And6'  # 'От 3 до 6 лет'
    MORE_THAN_6 = 'moreThan6'  # 'Более 6 лет'


class EducationLevel(Enum):
    SECONDARY = 'secondary'  # Среднее
    SPECIAL_SECONDARY = 'special_secondary'  # Среднее специальное
    UNFINISHED_HIGHER = 'unfinished_higher'  # Незаконченное высшее
    BACHELOR = 'bachelor'  # Бакалавр
    MASTER = 'master'  # Магистр
    HIGHER = 'higher'  # Высшее


class EmploymentType(Enum):
    """Используется для получения employment в фильтрации поиска резюме"""
    FULL = "full"  # 'Полная занятость'
    PART = "part"  # 'Частичная занятость'
    PROJECT = "project"  # 'Проектная работа'
    VOLUNTEER = "volunteer"  # 'Волонтерство'
    PROBATION = "probation"  # 'Стажировка'


class WorkSchedule(Enum):
    FULL_DAY = 'fullDay'  # Полный день
    SHIFT = 'shift'  # Сменный график
    FLEXIBLE = 'flexible'  # Гибкий график
    REMOTE = 'remote'  # Удаленная работа
    FLY_IN_FLY_OUT = 'flyInFlyOut'  # Вахтовый метод


class LabelType(Enum):
    ONLY_WITH_PHOTO = 'only_with_photo'  # Только с фотографией
    ONLY_WITH_SALARY = 'only_with_salary'  # Не показывать резюме без зарплаты
    ONLY_WITH_AGE = 'only_with_age'  # Не показывать резюме без указания возраста
    ONLY_WITH_GENDER = 'only_with_gender'  # Не показывать резюме без указания пола
    ONLY_WITH_VEHICLE = 'only_with_vehicle'  # Есть личный автомобиль
    EXCLUDE_VIEWED_BY_USER_ID = 'exclude_viewed_by_user_id'  # Скрыть резюме, просмотренные мной
    EXCLUDE_VIEWED_BY_EMPLOYER_ID = 'exclude_viewed_by_employer_id'  # Скрыть резюме, просмотренные всей компанией
    ONLY_IN_RESPONSES = 'only_in_responses'  # Показать только из откликов и приглашений


class Gender(Enum):
    MALE = 'male'  # 'Мужской'
    FEMALE = 'female'  # 'Женский'
    ANY = None  # 'Любой'


class SalaryRange(NamedTuple):
    salary_to: int  # Максимальная зарплата
    salary_from: int  # Минимальная зарплата


class AgeRange(NamedTuple):
    age_from: int  # Минимальный возраст
    age_to: int  # Максимальный возраст
