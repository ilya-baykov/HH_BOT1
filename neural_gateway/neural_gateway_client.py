import json

from configuration_file_handler.file_dataclass import RecruiterDataParams
from configuration_file_handler.read_file import RecruiterDataReader
from logger import logger
from neural_gateway.prompt_generator import PromptGenerator
from neural_gateway.requests_func import post_request
from pdf_parser.pdf_reader import PDFTextExtractor


class NeuralGatewayClient:
    """Класс для подключения к нейрошлюзу и выполнения запросов к API нейросети."""

    # Приватное свойство для хранения токена авторизации.
    __TOKEN = ("eyJhbGciOiJIUzI1NiJ9.eyJzY29wZXMiOlsiY2hhdEdwdCIsImdpZ2FDaGF0Iiwib"
               "2NyIiwic2VhcmNoQnlGaWxlIiwieWFDaGF0IiwibWlzdHJhbCJdLCJzdWIiOiJSdGt"
               "LUyIsImlhdCI6MTcxNzY3NzE2NSwiZXhwIjoyNTgxNTkwNzY1fQ.A_Y-ZuXWP1wK06eZgMc0RaRiJcx0Tvhl3LYfHR_lmSc")

    # Заголовки HTTP запроса, включая авторизацию и тип контента.
    __HEADERS = {"Authorization": f"Bearer {__TOKEN}", "Content-Type": "application/json"}

    __URL = "https://ai.rt.ru/api/1.0/chatgpt/chat"

    def __init__(self, model="gpt-4o-mini", temperature=0):
        """
        Инициализация экземпляра класса NeuralGatewayClient.

        Args:
        - model (str): Модель нейросети для использования (по умолчанию "gpt-4o-mini").
        - temperature (float): Температура для генерации ответов (по умолчанию 0).

        """
        self.model = model
        self.temperature = temperature

    def __create_request(self, prompt) -> dict:
        """
        Формирует данные для отправки запроса к API.

        Args:
        - content (str): Входные данные от пользователя для обработки.

        Returns:
        - dict: Словарь с данными для запроса к API.
        """
        logger.info(f'Отправка текста в нейрошлюз: {prompt}')
        data = {
            "chat": {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "type": "msg"
                    }
                ],
                "model": self.model,
                "temperature": self.temperature
            }
        }
        return data

    def process_content(self, prompt: str):
        """
        Обрабатывает входные данные от пользователя.

        Args:
        - content (str): Строка данных от пользователя для обработки.

        Returns:
        - str: Результат обработки запроса к API или сообщение об ошибке.
        """
        try:
            data = self.__create_request(prompt)
            response = post_request(self.__URL, self.__HEADERS, json.dumps(data))

            if response.status_code == 200:
                response_data = response.json()
                if response_data and isinstance(response_data, list) and len(response_data) > 0:
                    return response_data[0]['message']['content']
                else:
                    return None
            else:
                return f"Ошибка при запросе к API. Код статуса: {response.status_code}"
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {e}")
            return None


model_gpt_4o_mini = NeuralGatewayClient()

pdf_path = r"C:\Users\ilyab\PycharmProjects\HH_BOT_1\pdf_parser\Бакулева Дарья Олеговна.pdf"
resume_text = PDFTextExtractor.get_text(pdf_path=pdf_path)

recruiter_params: RecruiterDataParams = RecruiterDataReader().read_data()

prompt = PromptGenerator.generate_prompt(recruiter_params=recruiter_params, resume_text=resume_text)

result_1 = model_gpt_4o_mini.process_content(prompt=prompt)
logger.info(result_1)
