from configuration_file_handler.file_dataclass import RecruiterDataParams


class PromptGenerator:
    @staticmethod
    def generate_prompt(recruiter_params: RecruiterDataParams, resume_text: str) -> str:
        prompt = f"""
               Проанализируй следующий текст резюме кандидата и оцени его соответствие требованиям вакансии по шкале от 1 до 100. Учитывай следующие параметры рекрутера:

               **Ключевые параметры (высокий приоритет):**
               - Вакансия: {recruiter_params.vacancy}
               - Название должности: {recruiter_params.job_title}
               - Необходимый опыт работы: {recruiter_params.required_experience}
               - Основные обязанности: {recruiter_params.main_responsibilities}
               - Пол (предпочтения): {recruiter_params.gender_preference}
               - Ожидаемая заработная плата: {recruiter_params.salary}

               Обязательно проанализируй предыдущий опыт работы кандидата, указанный в резюме. Обрати внимание на:
               - Соответствие опыта работы требованиям вакансии (отрасль, должности, уровень ответственности).
               - Наличие релевантных достижений и навыков, которые могут быть полезны для выполнения обязанностей по вакансии.
               - Длительность и стабильность предыдущих мест работы.

               **Текст резюме кандидата:**
               {resume_text}

               Пожалуйста, предоставь оценку соответствия кандидата требованиям вакансии и обоснуй свой вывод, учитывая приоритет ключевых параметров и анализ опыта работы.
               """
        return prompt.strip()