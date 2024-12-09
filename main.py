import os
from logger import logger

from configuration_file_handler.file_dataclass import RecruiterDataParams
from configuration_file_handler.read_file import RecruiterDataReader
from configuration_file_handler.enums_for_dataclass import *
from requests_handler.requests_manager import request_manager
from resumes_handler.resumes_handler import ResumesHandler


def main() -> None:
    # Получение справочной информации
    # response_reference_book = request_manager.reference_book_get.get_field_reference()

    # Получение информации о дневных лимитах
    limits = request_manager.get.get_day_limits(employer_id=os.getenv('EMPLOYER_ID'),
                                                manager_id=os.getenv('MANAGER_ID'))
    logger.info(f"На сегодня осталось:{limits.json().get('left')} лимитных запросов")

    # Данные из настроечного файла от рекрутера
    configuration_file_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\configuration_files\Копия Панченко_ДОСПГФ.xlsx"
    recruiter_params: RecruiterDataParams = RecruiterDataReader(file_path=configuration_file_path).read_data()

    salary_range = recruiter_params.salary_range
    age_range = recruiter_params.age_range

    text_params = recruiter_params.generate_text_params(phrases_list=recruiter_params.job_title,
                                                        logic=Logic.ANY, field=Field.EVERYWHERE,
                                                        period=Period.LAST_YEAR)
    # Формирование строки параметров
    params = {
        'page': 0,  # Номер страницы
        'per_page': 5,  # Количество резюме на странице
        'salary_from': salary_range.salary_from,  # Минимальная зарплата
        'salary_to': salary_range.salary_to,  # Максимальная зарплата
        'age_from': age_range.age_from,  # Минимальный возраст
        'age_to': age_range.age_to,  # Максимальный возраст
        'area': recruiter_params.search_territory,  # Регион поиска
        'relocation': Relocation.LIVING.value,  # Готовность к переезду
        'education_level': recruiter_params.education_level,  # Минимальный уровень образования
        'gender': recruiter_params.gender,  # Пол соискателя
        'job_search_status': recruiter_params.job_search_status,  # Статус поиска работы
        'employment': recruiter_params.employment,  # Тип занятости
        'experience': recruiter_params.experience,  # Опыт работы
        'schedule': recruiter_params.schedule,  # График работы
        'label': recruiter_params.label,  # Дополнительный фильтр
        'skill': recruiter_params.skills,  # id Ключевых умений
        'citizenship': '113',  # Гражданство (Россия)
    }
    # Удаляем пары, где значения равны None
    params = {key: value for key, value in params.items() if value is not None}

    # Получение подходящих резюме
    resumes_response = request_manager.get.get_resumes(text_params=text_params, params=params)

    # Обработчик резюме
    resumes_handler = ResumesHandler(resumes_response)
    # resumes_handler.resume_process_with_limits(recruiter_params)  # Израсходует лимит
    resumes_handler.resume_process_no_limits(recruiter_params)  # Не израсходует лимит


if __name__ == '__main__':
    main()
