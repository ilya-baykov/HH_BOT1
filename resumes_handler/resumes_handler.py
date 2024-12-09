import os

from requests import Response

from configuration_file_handler.file_dataclass import RecruiterDataParams
from logger import logger
from neural_gateway.neural_gateway_client import model_gpt_4o_mini
from neural_gateway.prompt_generator import PromptGenerator
from pdf_parser.download_pdf import PDFDownloader
from pdf_parser.pdf_reader import PDFTextExtractor
from pdf_parser.text_writer import TextWriter
from requests_handler.requests_manager import request_manager


class ResumesHandler:
    def __init__(self, resumes_response: Response):
        """
        Инициализирует обработчик резюме, извлекая список резюме из ответа.

        :param resumes_response: Ответ от запроса, содержащий список резюме.
        """

        try:
            self.resumes_list: list[dict] = resumes_response.json().get('items')
        except Exception as e:
            self.resumes_list = []
            logger.error(f"При попытке получить резюме из запроса - произошла ошибка {e}")

    def resume_process_no_limits(self, recruiter_params: RecruiterDataParams):
        for resume in self.resumes_list:
            resume_text = (f"Желаемая должность - {resume.get('title')}"
                           f"\nСписок сертификатов - {resume.get('certificate')}"
                           f"\nОбщий стаж - {resume.get('total_experience')}"
                           f"\nОпыт работы - {resume.get('experience')}"
                           f"\nТеги к резюме - {resume.get('tags')}")

            prompt = PromptGenerator.generate_prompt(recruiter_params=recruiter_params,
                                                     resume_text=resume_text)
            result_1 = model_gpt_4o_mini.get_answer(prompt=prompt)
            logger.info(result_1)

    def resume_process_with_limits(self, recruiter_params: RecruiterDataParams):
        for resume in self.resumes_list:
            try:
                resume_pdf_url = resume['actions']['download']['pdf']['url']
            except KeyError:
                continue

            download_response = request_manager.get.download_pdf(pdf_url=resume_pdf_url)
            pdf_downloader = PDFDownloader(vacancy_id=str(recruiter_params.application_number),
                                           recruiter_surname=recruiter_params.fio_recruiter,
                                           candidate_surname=resume.get('last_name') or resume.get('title'))
            pdf_downloader.download(download_response)

            resume_text = PDFTextExtractor.get_text(pdf_path=pdf_downloader.resume_pdf_path)

            prompt = PromptGenerator.generate_prompt(recruiter_params=recruiter_params,
                                                     resume_text=resume_text)
            gpt_answer = model_gpt_4o_mini.get_answer(prompt=prompt)
            logger.info(gpt_answer)

            # Сохраняем результат обработки в виде txt-файла в папке с pdf-резюме
            TextWriter.write_pdf(file_path=os.path.join(pdf_downloader.folder_path, 'verdict.txt'), content=gpt_answer)
