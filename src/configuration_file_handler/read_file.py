import pandas as pd
from src.configuration_file_handler.file_dataclass import RecruiterDataParams
from src.configuration_file_handler.validators import *
from config.constants.paths import CONFIGURATION_FILES_PATH


class RecruiterDataReader:
    def __init__(self, file_path: str = CONFIGURATION_FILES_PATH):
        self.file_path = file_path

    def read_data(self) -> RecruiterDataParams:
        df = pd.read_excel(self.file_path)  # Чтение таблицы из Excel файла

        # Извлечение значений из второго и четвертого столбцов
        keys = df.iloc[1:, 1]  # Значения из второго столбца (начиная со второй строки)
        values = df.iloc[1:, 3]  # Значения из четвертого столбца (начиная со второй строки)

        # Создание словаря
        row = dict(zip(keys, values))

        return RecruiterDataParams(
            limit=20,
            fio_recruiter=row.get('ФИО рекрутера (полностью)'),
            email_recruiter=row.get('Почта рекрутера'),
            application_number=row.get('Номер заявки в IQHR/ссылка на заявку'),
            vacancy=row.get('Вакансия по штатной книге (если создана вне штатной книги, указать как в IQHR)'),

            region=row.get('Регион (территория поиска)'),
            city=row.get('Город (место трудоустройства)'),

            job_title=row.get('Название должности (ключевые слова или варианты поиска)'),
            main_responsibilities=row.get('Основные обязанности (ключевые слова)'),

            education=education_choice_validator.validate(row.get('Образование (минимальный уровень)')),

            search_status=row.get('Статус поиска'),

            additional_education=row.get('Дополнительное образование (Наличие сертификатов, лицензий)'),

            required_experience=row.get('Необходимый опыт работы (отрасль, должности, уровень ответственности и др.)'),

            employment_type_full_time=binary_choice_validator.validate(row.get('Тип занятости: Полная занятость')),

            employment_type_part_time=binary_choice_validator.validate(
                row.get('Тип занятости: Частичная занятость')),

            employment_type_project=binary_choice_validator.validate(
                row.get('Тип занятости: Проектная работа/разовое задание')),

            employment_type_internship=binary_choice_validator.validate(row.get('Тип занятости: Стажировка')),
            work_schedule_full_day=binary_choice_validator.validate(row.get('График работы: Полный день')),
            work_schedule_shift=binary_choice_validator.validate(row.get('График работы: Сменный график')),
            work_schedule_flexible=binary_choice_validator.validate(row.get('График работы: Гибкий график')),
            work_schedule_remote=binary_choice_validator.validate(row.get('График работы: Удаленная работа')),
            work_schedule_rotational=binary_choice_validator.validate(row.get('График работы: Вахтовый метод')),

            salary=row['Заработная плата'],

            age=row['Возраст'],

            gender_preference=gender_choice_validator.validate(row.get('Пол (предпочтения руководителя)')),
            citizenship=citizenship_choice_validator.validate(row.get('Гражданство (всегда указывается Россия)')),
            work_experience=row['Стаж работы (с опытом (другие варианты)\\без опыта (HH.ru не имеет значения)'],
            software_knowledge=row['Знание\\владение ПО (ключевые требования к владению ПО)'],

            specialization=row.get(
                'Специализация (указать из справочника специализации HH.ru, если не требуется - оставить поле пустым)'),

            show_resume_without_salary=binary_choice_validator.validate(
                row.get('Показывать резюме без указания зарплаты')),
            resume_view_depth=row['Глубина просмотра резюме на HH.ru в днях'],
            exclude_resume_keywords=row.get('Требуется ли исключить резюме из поиска по ключевым словам'),
            exclude_keywords=row.get('Слова, с которыми робот не должен искать резюме'),

            exclude_resume_phrases=exclusion_criteria_choice_validator.validate(
                row.get('Исключать резюме, в которых содержатся:')),

            exclude_keywords_in=row.get(
                'Ключевые слова для исключения содержатся (п. 26 Обязательно для заполнения, '
                'если в строке 32 указано "Да")', '').split(','),
            exclude_in_everywhere=row.get('Везде'),
            exclude_in_resume_title=row.get('В названии резюме'),
            exclude_in_education=row.get('В образовании'),
            exclude_in_skills=row.get('В ключевых навыках'),
            exclude_in_work_experience=row.get('В опыте работы')
        )
