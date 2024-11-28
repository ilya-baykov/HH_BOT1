from enum import Enum


class BinaryChoice(Enum):
    YES = "Да"
    NO = "Нет"


class Gender(Enum):
    MALE = "Мужчина"
    FEMALE = "Женщина"
    ANY = "Любой"


# Перечисление для вариантов исключения резюме
class ExclusionCriteria(Enum):
    ALL_WORDS = "Все слова"
    ANY_WORD = "Любое из слов"
    EXACT_PHRASE = "Точная фраза"
    NOT_PRESENT = "Не встречается"
