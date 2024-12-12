class InvalidLiteralValueError(Exception):
    def __init__(self, value: str, valid_values: tuple):
        super().__init__(f"Значение '{value}' не является допустимым. Допустимые значения: {valid_values}")
        self.value = value
        self.valid_values = valid_values


class MissingParameterError(Exception):
    pass
