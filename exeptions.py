class EnvFileLoadError(Exception):
    """Исключение, возникающее при ошибке загрузки файла .env."""
    pass


class TokenNotFoundError(Exception):
    """Исключение, возникающее при отсутствии токена."""
    pass


class TokenManagerError(Exception):
    """Исключение для ошибок в TokenManager."""
    pass
