from dataclasses import dataclass
from typing import Optional, Any


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
    skills: Optional[str]
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

    photo_link: Optional[str] = None  # Ссылка на фотографию кандидата

    @property
    def data_to_save_db(self) -> dict[str, Any]:
        """Возвращает данные для сохранения в БД"""
        data_to_insert = {
            "resume_id": str(self.id),
            "resume_url": self.url,
            "pdf_path": self.pdf_path,
            "resume_title": self.title,
            "salary": int(self.salary),
            "last_experience": str(self.last_experience),  # Преобразование в строку
            "total_experience_months": int(self.total_experience.get('months', 0)) if self.total_experience else 0,
            "education_level": self.education_level,
            "age": int(self.age) if self.age else 0,
            "gender": self.gender,
            "region": self.area,
            "rating_1": int(self.grade_1),
            "justification_1": self.justification_1,
            "rating_2": int(self.grade_2),
            "justification_2": self.justification_2}
        return data_to_insert
