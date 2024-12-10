from dataclasses import dataclass
from typing import Optional


@dataclass
class Applicant:
    """Данные о соискателе"""
    url: str  # Ссылка на резюме
    id: str  # id резюме
    title: str  # Название резюме
    pdf_url_download: Optional[str]  # Ссылка на скачивание pdf
    pdf_path: Optional[str]  # Путь к резюме на сетевом ресурсе

    salary: Optional[int]  # Желаемая зарплата
    last_experience: dict[str, int]  # Последнее место работы (доступно в безлимитных запросах)
    total_experience: Optional[dict[str, int]]  # Общий стаж(доступен в лимитных запросах)
    tags: Optional[list]  # Тэки к резюме

    education_level: Optional[str]  # Уровень образования
    certificate: Optional[list]  # Различные сертификаты

    gender: Optional[str]  # Пол
    age: Optional[str]  # Возраст
    area: Optional[str]  # Город проживания

    grade_1: int  # Результат первичной проверки
    justification_1: int  # Обоснование первичной проверки

    grade_2: Optional[int] = None  # Результат вторичной проверки
    justification_2: Optional[int] = None  # Обоснование вторичной проверки

    last_name: Optional[str] = None  # Фамилия
    first_name: Optional[str] = None  # Имя
    contact_phone: Optional[str] = None  # Контактный номер телефона
    sites_links: Optional[str] = None  # Ссылки на соц-сети
