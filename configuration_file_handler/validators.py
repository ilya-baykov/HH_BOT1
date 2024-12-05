from configuration_file_handler.exeptions import InvalidLiteralValueError


class LiteralValidator:
    """Класс для валидации строковых значений на соответствие заданному литералу."""

    def __init__(self, valid_values: tuple[str, ...]):
        """
        Инициализация класса
        :param valid_values: допустимые значения.
        """
        self.valid_values = valid_values

    def validate(self, value: str) -> str:
        """
        Проверяет, содержится ли переданное значение в допустимых значениях.

        Параметры:
        value (str): Значение, которое необходимо проверить.

        Исключения:
        InvalidLiteralValueError: Если значение не содержится в допустимых значениях.
        """
        if isinstance(value, str):
            value_lower = value.lower()
            if value_lower not in self.valid_values:
                raise InvalidLiteralValueError(value_lower, self.valid_values)
            else:
                return value


binary_choice_validator = LiteralValidator(("да", "нет"))

gender_choice_validator = LiteralValidator(("любой",
                                            "мужской",
                                            "женский"))

education_choice_validator = LiteralValidator(("среднее",
                                               "среднее специальное",
                                               "незаконченное высшее",
                                               "бакалавр",
                                               "магистр",
                                               "высшее"))

citizenship_choice_validator = LiteralValidator(("россия",))

exclusion_criteria_choice_validator = LiteralValidator(("все слова",
                                                        "любое из слов",
                                                        "точная фраза",
                                                        "не встречается"))
