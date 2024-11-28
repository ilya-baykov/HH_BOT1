import os
from loguru import logger

# Создаем папку LOGS, если она не существует

# Определяем корневой путь проекта
root_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем папку LOGS, если она не существует
log_dir = os.path.join(root_dir, "LOGS")
os.makedirs(log_dir, exist_ok=True)

# Настройка логирования
logger.add(
    os.path.join(log_dir, "log_{time:YYYY-MM-DD}.log"),  # Логи за день
    rotation="1 day",  # Ротация по дням
    compression="zip",  # Архивировать логи каждую неделю
    level="DEBUG",  # Уровень логирования
    format="{time:MM-DD at HH:mm:ss} | {level} | {message} | {name}:{function}:{line}"  # Формат сообщения
)
