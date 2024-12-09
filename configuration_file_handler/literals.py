from typing import Literal

# литералы для бинарного выбора
BinaryChoiceLiteral = Literal["Да", "Нет"]

# литералы для выбора минимального уровня образования
EducationLevelLiteral = Literal[
    "Среднее",
    "Среднее специальное",
    "Незаконченное высшее",
    "Бакалавр",
    "Магистр",
    "Высшее"
]

GenderLiteral = Literal[
    "Любой",
    "Мужской",
    "Женский"
]

CitizenshipLiteral = Literal[
    "Россия"
]
ExclusionCriteriaLiteral = Literal[
    "Все слова",
    "Любое из слов",
    "Точная фраза",
    "Не встречается",
]
