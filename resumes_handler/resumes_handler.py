import os

from requests import Response

from configuration_file_handler.file_dataclass import RecruiterDataParams
from database.operations import db_operations
from logger import logger
from neural_gateway.neural_gateway_client import model_gpt_4o_mini
from neural_gateway.prompt_generator import PromptGenerator
from pdf_parser.download_pdf import PDFDownloader
from pdf_parser.pdf_reader import PDFTextExtractor
from pdf_parser.text_writer import TextWriter
from requests_handler.requests_manager import request_manager
from resumes_handler.applicant_info import Applicant
from resumes_handler.json_extractor import JsonExtractor


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

    def resume_process_no_limits(self, recruiter_params: RecruiterDataParams) -> list[Applicant]:
        applicants = []

        for resume in self.resumes_list:
            # fetched_resume_id = db_operations.fetch_data(table_name="resume_reports_new", column_name='resume_id',
            #                                              value=resume.get('id'))
            # if fetched_resume_id:  # Это резюме уже есть в базе данных
            #     continue
            try:
                # Извлекаем информацию с последнего места работы
                last_experience = resume.get('experience', [{}])[0]
                last_experience_info = {key: last_experience.get(key, 'Не указано') for key in
                                        ['start', 'end', 'company', 'position']}
                # Извлекаем информацию об образовании
                education_level_name = resume.get('education', {}).get('level', {}).get('name', 'Не указано')

                # Формирует данные для генерации промпта нейросети
                resume_text = (
                    f"Желаемая должность - {resume.get('title', 'Не указано')}\n"
                    f"Уровень образования - {education_level_name}\n"
                    f"Список сертификатов - {resume.get('certificate', 'Нет')}\n"
                    f"Последнее место работы - {last_experience_info}\n"
                    f"Теги к резюме - {resume.get('tags', 'Отсутствуют')}"
                )

                prompt = PromptGenerator.generate_primary_prompt(recruiter_params=recruiter_params,
                                                                 resume_text=resume_text)
                # Очищаем ответ от нейросети
                not_peeled_answer = model_gpt_4o_mini.get_answer(prompt=prompt)
                clear_answer_json = JsonExtractor.extract_json(not_peeled_answer)

                # Сохраняем первичную информацию о кандидате
                applicant = Applicant(
                    url=resume.get('url'),
                    id=resume.get('id'),
                    title=resume.get('title', 'Не указано'),
                    salary=resume.get('salary', {}).get('amount', 'Не указано'),
                    last_experience=last_experience_info,
                    education_level=education_level_name,
                    certificate=resume.get('certificate', 'Не указаны'),
                    last_name=resume.get('last_name'),
                    first_name=resume.get('first_name'),
                    gender=resume.get('gender', {}).get('id'),
                    age=resume.get('age', 'Не указано'),
                    area=resume.get('area', {}).get('name'),
                    grade_1=clear_answer_json.get('grade', "Ошибка"),
                    justification_1=clear_answer_json.get('justification', "Ошибка"),
                    tags=resume.get('tags', 'Отсутствуют'),
                    pdf_url_download=resume['actions']['download']['pdf']['url'],
                    pdf_path=None, total_experience=None
                )

                logger.info(applicant)
                applicants.append(applicant)

            except Exception as e:
                logger.error(f"При первичном оценивании резюме {resume.get('id')} - произошла ошибка: {e}")

        return applicants

    @staticmethod
    def resume_process_with_limits(sorted_applicants: list[Applicant], recruiter_params: RecruiterDataParams):
        applicants = []

        for applicant in sorted_applicants:  # Обходим список потенциальных кандидатов

            # Загружаем и обрабатываем PDF
            download_response = request_manager.get.download_pdf(pdf_url=applicant.pdf_url_download)
            pdf_downloader = PDFDownloader(vacancy_id=str(recruiter_params.application_number),
                                           recruiter_surname=recruiter_params.fio_recruiter,
                                           candidate_surname=applicant.last_name or applicant.title)
            pdf_downloader.download(download_response)

            resume_text = PDFTextExtractor.get_text(pdf_path=pdf_downloader.resume_pdf_path)

            # Формируем промпт для нейросети
            prompt = PromptGenerator.generate_grand_prompt(recruiter_params=recruiter_params,
                                                           resume_text=resume_text)

            # Получаем ответ от нейросети
            not_peeled_answer = model_gpt_4o_mini.get_answer(prompt=prompt)
            if not_peeled_answer:
                clear_answer_json = JsonExtractor.extract_json(not_peeled_answer)

                logger.info(clear_answer_json)
                applicant.pdf_path = pdf_downloader.resume_pdf_path
                applicant.grade_2 = clear_answer_json.get('grade')
                applicant.justification_2 = clear_answer_json.get('justification')

                # Сохраняем результат обработки в виде txt-файла в папке с pdf-резюме
                TextWriter.write_pdf(file_path=os.path.join(pdf_downloader.folder_path, 'verdict.txt'),
                                     content=not_peeled_answer)
                applicants.append(applicant)

        return applicants
