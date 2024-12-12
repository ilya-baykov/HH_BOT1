import os
from datetime import datetime

import openpyxl

from src.resumes_handler.applicant_info import Applicant


class ReportGenerator:
    HEADERS = [
        "ID", "URL", "Название Резюме", "PDF URL", "PDF Путь", "Зарплата",
        "Последний опыт", "Общий опыт (мес.)", "Уровень образования",
        "Пол", "Возраст", "Регион", "Оценка 1",
        "Обоснование 1", "Оценка 2", "Обоснование 2"
    ]

    def __init__(self, candidates: list[Applicant], path: str):
        self.candidates = candidates
        self.path = path

    def generate_report(self):

        # Формируем имя файла с текущей датой в формате ММ.ГГГГ
        current_date = datetime.now().strftime("%m.%Y")  # Получаем дату в формате ММ.ГГГГ
        report_filename = f"Потенциальные кандидаты {current_date}.xlsx"
        report_filepath = os.path.join(self.path, report_filename)

        # Проверяем, существует ли директория, если нет - создаем
        os.makedirs(self.path, exist_ok=True)

        # Проверяем, существует ли файл
        if os.path.exists(report_filepath):
            # Если файл существует, открываем его
            wb = openpyxl.load_workbook(report_filepath)
            ws = wb.active
        else:
            # Если файл не существует, создаем новый
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Кандидаты"
            ws.append(self.HEADERS)

        # Записываем данные о каждом кандидате
        for candidate in self.candidates:
            last_experience = f"{candidate.last_experience.get('position', '')} в {candidate.last_experience.get('company', '')}" if candidate.last_experience else ""
            total_experience = candidate.total_experience.get('months', ' ')

            row = [
                candidate.id,
                candidate.url,
                candidate.title,
                candidate.pdf_url_download,
                candidate.pdf_path,
                candidate.salary,
                last_experience,
                total_experience,
                candidate.education_level,
                ", ".join(candidate.certificate) if candidate.certificate else "",
                candidate.gender,
                candidate.age,
                candidate.area,
                candidate.grade_1,

                candidate.justification_1,
                candidate.grade_2,
                candidate.justification_2,

            ]

            ws.append(row)

            # Сохраняем файл
        wb.save(report_filepath)
        print(f"Отчет сохранен по пути: {report_filepath}")
