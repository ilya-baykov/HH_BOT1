from enum import Enum


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
