import os

import uvicorn

from configuration_file_handler.file_dataclass import RecruiterDataParams
from configuration_file_handler.read_file import RecruiterDataReader
from neural_gateway.neural_gateway_client import ChatGPT, YaGPT
from neural_gateway.prompt_generator import PromptGenerator
from pdf_parser.pdf_reader import PDFTextExtractor

from logger import logger
from requests_handler.fast_api import app
from requests_handler.requests_manager import request_manager


def main() -> None:
    response_reference_book = request_manager.reference_book_get.get_field_reference()

    limits = request_manager.get.get_day_limits(employer_id=os.getenv('EMPLOYER_ID'),
                                                manager_id=os.getenv('MANAGER_ID'))

    configuration_file_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\configuration_files\Клепач_Оператор call-центра_308119.xlsx"
    recruiter_params: RecruiterDataParams = RecruiterDataReader(file_path=configuration_file_path).read_data()

    # vladimir_areas = request_manager.reference_book_get.get_areas(text="Владимир")
    # nizniy_novgorod_areas = request_manager.reference_book_get.get_areas(text="Нижний Новгород")

    resumes = request_manager.get.get_resumes(
        salary_from=200_000,
        salary_to=300_000,
        page=3,
        per_page=15,
        area=['23', '66'],  # Список регионов
        relocation='living'  # Только те, кто живет в указанном регионе
    )
    print(resumes)
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
