from dataclasses import dataclass, field
from typing import List, Optional

from configuration_file_handler.enums_for_dataclass import BinaryChoice, Gender, ExclusionCriteria


@dataclass
class RecruiterDataParams:
    fio_recruiter: str  # ФИО рекрутера (полностью)
    email_recruiter: str  # Почта рекрутера
    application_number: str  # Номер заявки в IQHR/ссылка на заявку
    vacancy: str  # Вакансия по штатной книге

    region: str  # Регион (территория поиска)
    city: str  # Город (место трудоустройства)

    job_title: str  # Название должности (ключевые слова или варианты поиска)
    main_responsibilities: str  # Основные обязанности (ключевые слова)

    education: Optional[str]  # Образование (минимальный уровень)

    search_status: Optional[str]  # Статус поиска

    additional_education: Optional[str]  # Дополнительное образование (Наличие сертификатов, лицензий)

    required_experience: str  # Необходимый опыт работы (отрасль, должности, уровень ответственности и др.)

    employment_type_full_time: str | BinaryChoice  # Тип занятости: Полная занятость
    employment_type_part_time: str | BinaryChoice  # Тип занятости: Частичная занятость
    employment_type_project: str | BinaryChoice  # Тип занятости: Проектная работа/разовое задание
    employment_type_internship: str | BinaryChoice  # Тип занятости: Стажировка
    work_schedule_full_day: str | BinaryChoice  # График работы: Полный день
    work_schedule_shift: str | BinaryChoice  # График работы: Сменный график
    work_schedule_flexible: str | BinaryChoice  # График работы: Гибкий график
    work_schedule_remote: str | BinaryChoice  # График работы: Удаленная работа
    work_schedule_rotational: str | BinaryChoice  # График работы: Вахтовый метод

    salary: str  # Заработная плата

    age: str  # Возраст

    gender_preference: Optional[Gender]  # Пол (предпочтения руководителя)

    citizenship: str  # Гражданство (всегда указывается Россия)

    work_experience: str  # Стаж работы (с опытом/без опыта)

    software_knowledge: str  # Знание/владение ПО (ключевые требования к владению ПО)

    specialization: Optional[str]  # Специализация (указать из справочника специализации, если не требуется - None)

    show_resume_without_salary: str | BinaryChoice  # Показывать резюме без указания зарплаты

    resume_view_depth: str  # Глубина просмотра резюме на HH.ru в днях

    exclude_resume_keywords: str | BinaryChoice  # Требуется ли исключить резюме из поиска по ключевым словам
    exclude_keywords: Optional[str]  # Слова, с которыми робот не должен искать резюме
    exclude_resume_phrases: Optional[str | ExclusionCriteria]  # Исключать резюме, в которых содержатся
    exclude_keywords_in: List[str]  # Ключевые слова для исключения содержатся
    exclude_in_everywhere: Optional[str | BinaryChoice]  # Везде
    exclude_in_resume_title: Optional[str | BinaryChoice]  # В названии резюме
    exclude_in_education: Optional[str | BinaryChoice]  # В образовании
    exclude_in_skills: Optional[str | BinaryChoice]  # В ключевых навыках
    exclude_in_work_experience: Optional[str | BinaryChoice]  # В опыте работы

