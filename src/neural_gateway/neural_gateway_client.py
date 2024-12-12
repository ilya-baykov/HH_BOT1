import json
from abc import ABC, abstractmethod
from typing import Optional

import requests
from requests import Response
from config.logger import logger
from src.neural_gateway.requests_func import post_request


class NeuralGatewayClient(ABC):
    BASE_URL = "https://ai.rt.ru/api/1.0"  # Основной путь url нейрошлюза для разных моделей

    # Приватное свойство для хранения токена авторизации.
    __TOKEN = ("eyJhbGciOiJIUzI1NiJ9.eyJzY29wZXMiOlsiY2hhdEdwdCIsImdpZ2FDaGF0Iiwib"
               "2NyIiwic2VhcmNoQnlGaWxlIiwieWFDaGF0IiwibWlzdHJhbCJdLCJzdWIiOiJSdGt"
               "LUyIsImlhdCI6MTcxNzY3NzE2NSwiZXhwIjoyNTgxNTkwNzY1fQ.A_Y-ZuXWP1wK06eZgMc0RaRiJcx0Tvhl3LYfHR_lmSc")

    # Заголовки HTTP запроса, включая авторизацию и тип контента.
    __HEADERS = {"Authorization": f"Bearer {__TOKEN}", "Content-Type": "application/json"}

    TEMPERATURE = 0
    URL = None

    def __init__(self):
        if not hasattr(self, 'URL'):
            raise NotImplementedError("Класс-наследник должен определить атрибут URL и он не должен быть None.")

    def get_answer(self, prompt: str):
        request_data = self._create_data_request(prompt=prompt)
        response: Response = self._get_response(request_data=request_data)

        try:
            response_data = response.json()
            if response_data and isinstance(response_data, list) and len(response_data) > 0:
                message_content = response_data[0]['message']['content']
                return message_content
        except Exception as e:
            logger.error(f"При попытке получить ответ от нейрошлюза произошла ошибка: {e}")

    @abstractmethod
    def _create_data_request(self, prompt: str):
        """
            Формирует данные для отправки запроса к API.

            Args:
            - content (str): Входные данные от пользователя для обработки.

            Returns:
            - dict: Словарь с данными для запроса к API.
            """
        pass

    def _get_response(self, request_data: dict) -> Optional[Response]:
        """
        Обрабатывает входные данные от пользователя.

        Args:
        - prompt (str): Строка данных от пользователя для обработки (промпт).

        Returns:
        - str: Результат обработки запроса к API или сообщение об ошибке.
        """
        try:
            response = post_request(self.URL, self.__HEADERS, json.dumps(request_data))
            response.raise_for_status()  # Проверяем статус ответа
            logger.info(f"{self.URL}. Статус - {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"{self.URL}.Произошла ошибка: {e}")
            return None
        except Exception as e:
            logger.error(f"{self.URL}.Произошла неизвестная ошибка: {e}")


class ChatGPT(NeuralGatewayClient):
    MODEL = "gpt-4o-mini"
    URL = f"{NeuralGatewayClient.BASE_URL}/chatgpt/chat"

    def _create_data_request(self, prompt: str) -> dict:
        data = {
            "chat": {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "type": "msg"
                    }
                ],
                "model": self.MODEL,
                "temperature": self.TEMPERATURE
            }
        }
        logger.debug(f'Сформированные данные для запроса к нейрошлюзу: {data}')
        return data


class YaGPT(NeuralGatewayClient):
    MODEL = "yandexgpt-lite"
    URL = f"{NeuralGatewayClient.BASE_URL}/ya/chat"

    def _create_data_request(self, prompt: str) -> dict:
        data = {
            "chat": {
                "model": self.MODEL,
                "messages": [
                    {
                        "role": "user",
                        "text": prompt
                    }
                ],
                "completionOptions": {
                    "temperature": self.TEMPERATURE
                }
            }
        }
        logger.debug(f'Сформированные данные для запроса к нейрошлюзу: {data}')
        return data


model_gpt_4o_mini = ChatGPT()
