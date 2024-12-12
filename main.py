import os
import pandas as pd
import config.env_loader  # Необходим для загрузки переменных окуржения вначале программы
from config.constants.paths import RESUMES_ROOT_PATH
from src.configuration_file_handler.bypassing_configuration_files import ConfigurationFilesHandler
from src.configuration_file_handler.params_creator import ParamsCollector
from src.database.database import report_database
from src.database.operations import db_operations
from src.report_generator.report_generator import ReportGenerator
from src.requests_handler.requests_manager import request_manager
from config.logger import logger
from src.resumes_handler.applicant_info import Applicant
from src.resumes_handler.contact_recipient import CandidateInfoRecipient
from src.resumes_handler.resumes_handler import ResumesHandler


@logger.catch
def main() -> None:
    configuration_files_handler = ConfigurationFilesHandler()

    # Обход настроечных файлов
    for recruiter_params in configuration_files_handler.bypassing_files():
        # Фиксация дневных лимитов
        limits_response = request_manager.get.get_day_limits(employer_id=os.getenv('EMPLOYER_ID'),
                                                             manager_id=os.getenv('MANAGER_ID'))
        logger.info(f"Дневные лимиты: {limits_response.json()}" if limits_response.status_code
                    else "Не получилось узнать дневные лимиты")

        # Параметры для фильтрации кандидатов
        params_creator = ParamsCollector(recruiter_params=recruiter_params)

        # Получение списка отфильтрованных резюме
        resumes_response = request_manager.get.get_resumes(text_params=params_creator.get_text_search,
                                                           params=params_creator.get_params)

        # Обработчик резюме
        resumes_handler = ResumesHandler(resumes_response)

        # Первичный сбор информации из резюме (с первичной оценкой на релевантность)
        applicants = resumes_handler.resume_process_no_limits(recruiter_params)  # Не израсходует лимит

        # Фильтрация и сортировка кандидатов
        sorted_applicants = sorted([candidate for candidate in applicants if candidate.grade_1 > 40],
                                   key=lambda x: x.grade_1,
                                   reverse=True)

        sorted_applicants = sorted_applicants[:recruiter_params.limit]
        logger.info(f"Количество потенциальных кандидатов после первичной проверки: {len(sorted_applicants)}")

        # Вторичный сбор информации из резюме (с финальной оценкой на релевантность)
        applicants = resumes_handler.resume_process_with_limits(sorted_applicants, recruiter_params)  # расходует лимит

        # Фильтрация и сортировка кандидатов
        sorted_applicants = sorted(applicants, key=lambda x: (x.grade_2 is None, -x.grade_2))
        logger.info(f"Количество потенциальных кандидатов после вторичной проверки: {len(sorted_applicants)}")

        # Получение детальной информации
        candidates: list[Applicant] = CandidateInfoRecipient(applicants=sorted_applicants).get_candidates

        # При успешном поиске новых кандидатов ( тех, котороые не добавляли в отчёты раньше )
        if candidates:
            # Формируем путь: "C:\\resumes" + Фамилия рекрутера + Номер вакансии
            base_path = os.path.join(RESUMES_ROOT_PATH, recruiter_params.fio_recruiter.strip(),
                                     str(recruiter_params.application_number))
            # Запись данных в отчёт
            report_generator = ReportGenerator(candidates=candidates, path=base_path)
            report_generator.generate_report()

            # Формируем данныек для сохранения в Таблицу Базы Данных
            data_to_save: pd.DataFrame = pd.DataFrame([
                {**candidate.data_to_save_db,
                 'recruiter_full_name': recruiter_params.fio_recruiter,
                 'job_number': recruiter_params.vacancy}
                for candidate in candidates
            ])

            # Сохраняем данные в БД
            report_database.connect()
            db_operations.insert_data_from_dataframe(db=report_database, auto_close=True,
                                                     table_name="public.resume_reports",
                                                     data=data_to_save)


if __name__ == '__main__':
    main()
