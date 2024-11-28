import pandas as pd
from configuration_file_handler.file_dataclass import RecruiterDataParams
from constants.paths import CONFIGURATION_FILE_PATH


class RecruiterDataReader:
    def __init__(self, file_path: str = CONFIGURATION_FILE_PATH):
        self.file_path = file_path

    def read_data(self) -> RecruiterDataParams:
        df = pd.read_excel(self.file_path)  # Чтение таблицы из Excel файла

        # Извлечение значений из второго и четвертого столбцов
        keys = df.iloc[1:, 1]  # Значения из второго столбца (начиная со второй строки)
        values = df.iloc[1:, 3]  # Значения из четвертого столбца (начиная со второй строки)

        # Создание словаря
        row = dict(zip(keys, values))

        return RecruiterDataParams(
            fio_recruiter=row.get('ФИО рекрутера (полностью)'),
            email_recruiter=row.get('Почта рекрутера'),
            application_number=row.get('Номер заявки в IQHR/ссылка на заявку'),
            vacancy=row.get('Вакансия по штатной книге (если создана вне штатной книги, указать как в IQHR)'),
            region=row.get('Регион (территория поиска)'),
            city=row.get('Город (место трудоустройства)'),
            job_title=row.get('Название должности (ключевые слова или варианты поиска)'),
            main_responsibilities=row.get('Основные обязанности (ключевые слова)'),
            education=row.get('Образование (минимальный уровень)', None),
            search_status=row.get('Статус поиска', None),
            additional_education=row.get('Дополнительное образование (Наличие сертификатов, лицензий)', None),
            required_experience=row['Необходимый опыт работы (отрасль, должности, уровень ответственности и др.)'],
            employment_type_full_time=row.get('Тип занятости: Полная занятость', 'Нет'),
            employment_type_part_time=row.get('Тип занятости: Частичная занятость', 'Нет'),
            employment_type_project=row.get('Тип занятости: Проектная работа/разовое задание', 'Нет'),
            employment_type_internship=row.get('Тип занятости: Стажировка', 'Нет'),
            work_schedule_full_day=row.get('График работы: Полный день', 'Нет'),
            work_schedule_shift=row.get('График работы: Сменный график', 'Нет'),
            work_schedule_flexible=row.get('График работы: Гибкий график', 'Нет'),
            work_schedule_remote=row.get('График работы: Удаленная работа', 'Нет'),
            work_schedule_rotational=row.get('График работы: Вахтовый метод', 'Нет'),
            salary=row['Заработная плата'],
            age=row['Возраст'],
            gender_preference=row.get('Пол (предпочтения руководителя)', None),
            citizenship=row['Гражданство (всегда указывается Россия)'],
            work_experience=row['Стаж работы (с опытом (другие варианты)\\без опыта (HH.ru не имеет значения)'],
            software_knowledge=row['Знание\\владение ПО (ключевые требования к владению ПО)'],
            specialization=row.get(
                'Специализация (указать из справочника специализации HH.ru, если не требуется - оставить поле пустым)',
                None),
            show_resume_without_salary=row.get('Показывать резюме без указания зарплаты', 'Нет'),
            resume_view_depth=row['Глубина просмотра резюме на HH.ru в днях'],
            exclude_resume_keywords=row.get('Требуется ли исключить резюме из поиска по ключевым словам', 'Нет'),
            exclude_keywords=row.get('Слова, с которыми робот не должен искать резюме', None),
            exclude_resume_phrases=row.get('Исключать резюме, в которых содержатся:', None),
            exclude_keywords_in=row.get(
                'Ключевые слова для исключения содержатся (п. 26 Обязательно для заполнения, если в строке 32 указано "Да")',
                '').split(','),
            exclude_in_everywhere=row.get('Везде', None),
            exclude_in_resume_title=row.get('В названии резюме', None),
            exclude_in_education=row.get('В образовании', None),
            exclude_in_skills=row.get('В ключевых навыках', None),
            exclude_in_work_experience=row.get('В опыте работы', None)
        )
