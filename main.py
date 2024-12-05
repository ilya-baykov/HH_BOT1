import os

import uvicorn
from urllib.parse import quote

from logger import logger
from configuration_file_handler.file_dataclass import RecruiterDataParams
from configuration_file_handler.read_file import RecruiterDataReader
from neural_gateway.neural_gateway_client import ChatGPT, YaGPT
from neural_gateway.prompt_generator import PromptGenerator
from pdf_parser.pdf_reader import PDFTextExtractor
from configuration_file_handler.enums_for_dataclass import *

from requests_handler.fast_api import app
from requests_handler.requests_manager import request_manager


def main() -> None:
    # Получение справочной информации
    response_reference_book = request_manager.reference_book_get.get_field_reference()
    response_professional_roles = request_manager.reference_book_get.get_professional_roles_reference()

    # # Получение информации о дневных лимитах
    limits = request_manager.get.get_day_limits(employer_id=os.getenv('EMPLOYER_ID'),
                                                manager_id=os.getenv('MANAGER_ID'))
    #
    # # Данные из настроечного файла от рекрутера
    configuration_file_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\configuration_files\Клепач_Оператор call-центра_308119.xlsx"
    recruiter_params: RecruiterDataParams = RecruiterDataReader(file_path=configuration_file_path).read_data()

    # Формирование строки параметров
    params = {
        # 'salary_from': 110_000,  # Минимальная зарплата
        # 'salary_to': 160_000,  # Максимальная зарплата
        # 'page': 3,  # Номер страницы
        # 'per_page': 15,  # Количество резюме на странице
        # 'area': ['23'],  # Регион поиска
        # 'relocation': 'living',  # Готовность к переезду
        # 'education_level': 'higher',  # Минимальный уровень образования
        # 'job_search_status': 'active_search',  # Статус поиска работы
        # 'age_from': "20",  # Минимальный возраст
        # 'age_to': "30",  # Максимальный возраст
        # 'employment': "full",  # Тип занятости
        # 'experience': "between3And6",  # Опыт работы
        # 'gender': "male",  # Пол соискателя
        # 'schedule': "remote",  # График работы
        # 'citizenship': '113',  # Гражданство
        # 'skill': '3018',  # Ключевые навыки
        # 'label': 'only_with_salary'  # Дополнительный фильтр
    }
    area = recruiter_params.search_territory
    text_params = recruiter_params.generate_text_params(phrases_list=recruiter_params.job_title,
                                                        logic=Logic.ANY, field=Field.EVERYWHERE,
                                                        period=Period.LAST_YEAR)

    # Получение подходящих резюме
    resumes = request_manager.get.get_resumes(text_params=text_params, params=params)

    print(resumes)
    # pdf_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\resumes\Менеджер по продажам_3.pdf"
    # resume_text = PDFTextExtractor.get_text(pdf_path=pdf_path)
    #
    # data_params_file_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\configuration_files\Менеджер дистанционных продаж.xlsx"
    # recruiter_params: RecruiterDataParams = RecruiterDataReader(file_path=data_params_file_path).read_data()
    #
    # prompt = PromptGenerator.generate_prompt(recruiter_params=recruiter_params, resume_text=resume_text)
    #
    # model_gpt_4o_mini = ChatGPT()
    # result_1 = model_gpt_4o_mini.get_answer(prompt=prompt)
    # logger.debug(f"Результат для модели model_gpt_4o_mini: ")
    # logger.info(result_1)
    #
    # model_ya_gpt = YaGPT()
    # result_2 = model_ya_gpt.get_answer(prompt=prompt)
    # logger.debug(f"Результат для модели YaGPT: ")
    # logger.info(result_2)


if __name__ == '__main__':
    main()
