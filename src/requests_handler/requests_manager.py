import os

import requests
import urllib3
from typing import Optional
from requests import Response

from config.constants.urls import HH_BASE_URL
from config.logger import logger
from src.requests_handler.token_manager import TokenManager

# Отключаем предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RequestsManager:
    def __init__(self, access_token: str):
        # Формируем путь к json файлу

        self.get = RequestsGet(access_token)
        self.post = RequestsPost(access_token)
        self.reference_book_get = ReferenceBookRequestsGet(access_token)


class RequestsBase:
    BASE_URL = HH_BASE_URL

    def __init__(self, access_token: str):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "HH-User-Agent": "RTK Resume Search (bot_podbor_oco@rt.ru)"
        }

    def _get_response(self, method: str, url: str, data: Optional[dict] = None, params: Optional[dict] = None,
                      headers: Optional[dict] = None, logger_message: str = "") -> Optional[Response]:
        headers = headers if isinstance(headers, dict) else self.headers
        data = data if isinstance(data, dict) else {}
        params = params if isinstance(params, dict) else {}

        if method.lower() == 'post':
            response = requests.post(url=url, headers=headers, data=data, verify=False)
        else:  # По умолчанию используем GET
            response = requests.get(url=url, headers=headers, params=params)
        try:
            response.raise_for_status()  # Проверяем статус ответа
            logger.debug(f"{logger_message}. Статус - {response.status_code}")
            return response
        except requests.exceptions.RequestException as error:
            logger.error(f"{logger_message}.Произошла ошибка: {error}")
            return None


class RequestsGet(RequestsBase):
    METHOD = "GET"

    def get_user_info(self):
        url = f"{self.BASE_URL}/me"
        response = self._get_response(method=self.METHOD, url=url,
                                      logger_message=f"Запрос на получение информации о пользователе")
        return response

    def get_day_limits(self, employer_id: str, manager_id: str):
        params = {'employer_id': employer_id, 'manager_id': manager_id}
        url = f"{self.BASE_URL}/employers/{employer_id}/managers/{manager_id}/limits/resume"
        response = self._get_response(method=self.METHOD, url=url,
                                      logger_message=f"Запрос на получение дневных лимитов просмотра резюме "
                                                     f"для текущего менеджера с параметрами: {params}")
        return response

    def get_resumes(self, text_params: str, params: dict):
        url = f"{HH_BASE_URL}/resumes?{text_params}"
        response = self._get_response(method=self.METHOD, url=url, params=params,
                                      logger_message=f"Запрос на получение резюме")
        return response

    def get_resume(self, resume_id: str):
        url = f"{HH_BASE_URL}/resumes/{resume_id}"
        response = self._get_response(method=self.METHOD, url=url,
                                      logger_message=f"Запрос на получение конкретного резюме")
        return response

    def download_pdf(self, pdf_url):
        response = self._get_response(method=self.METHOD, url=pdf_url,
                                      logger_message=f"Запрос на скачивание pdf-резюме")
        return response


class ReferenceBookRequestsGet(RequestsBase):
    METHOD = "GET"

    def get_areas(self, text: str):
        url = f"{HH_BASE_URL}/suggests/areas"
        params = {'text': text}
        response = self._get_response(method=self.METHOD, url=url, params=params,
                                      logger_message=f"Запрос на получение древовидного списка "
                                                     f"всех регионов для: {text} ")
        return response

    def get_field_reference(self):
        url = f"{HH_BASE_URL}/dictionaries/"
        response = self._get_response(method=self.METHOD, url=url,
                                      logger_message=f"Запрос на получение справочников полей и сущностей, "
                                                     f"применяемых в API.")
        return response

    def get_professional_roles_reference(self):
        url = f"{HH_BASE_URL}/professional_roles/"
        response = self._get_response(method=self.METHOD, url=url,
                                      logger_message=f"Запрос на получение справочной информации о "
                                                     f"профессиональных ролях, их категориях и другую информацию о "
                                                     f"профессиональных ролях")
        return response

    def get_skill_set(self, text: str):
        url = f"{HH_BASE_URL}/suggests/skill_set/"
        params = {'text': text}
        response = self._get_response(method=self.METHOD, url=url, params=params,
                                      logger_message=f"Запрос на получение ключевых навыков")
        return response


class RequestsPost(RequestsBase):
    METHOD = "POST"

    def get_access_token_application(self, client_id: str, client_secret: str) -> Optional[Response]:
        """
        Получает новый access-токен для приложения.

        Важно: данный метод следует использовать только в случае, если текущий токен был скомпрометирован.
        Данный access_token имеет неограниченный срок жизни. При повторном запросе ранее выданный токен
        отзывается и выдается новый. Запрашивать access_token можно не чаще, чем один раз в 5 минут.

        :param : Dict
            Словарь, содержащий следующие ключи:
            - client_id (str): Идентификатор, полученный при создании приложения.
            - client_secret (str): Защищенный ключ, полученный при создании приложения.

        :return: Optional[Response]
            Ответ от API, содержащий новый access-токен или информацию об ошибке.
        """
        data = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
        url = f"{self.BASE_URL}/token"
        response = self._get_response(method=self.METHOD, url=url, data=data,
                                      logger_message=f"Запрос на получение access-токена "
                                                     f"по параметрам:{data}")
        return response

    def get_access_token_user(self, client_id: str, client_secret: str, redirect_uri: str,
                              code: str) -> Optional[Response]:
        """Получает основной access-токен пользовтаеля для выполнения запросов

            Важно: данный метод следует использовать только в случае, если текущий токен был скомпрометирован.
            Данный access_token имеет время жизни 14 дней ( после нужно его обновлять )"""

        data = {'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'}

        url = f"{self.BASE_URL}/token"
        response = self._get_response(method=self.METHOD, url=url, data=data,
                                      logger_message=f"Запрос на получение access-токена "
                                                     f"по параметрам:{data}")
        return response

    def update_user_access_token(self, refresh_token: str) -> Optional[Response]:
        """
        Обновляет пары access и refresh токенов
        :param refresh_token: Refresh-токен, полученный ранее при получении пары токенов или прошлом обновлении пары
        """
        data = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        url = f"{self.BASE_URL}/token"
        response = self._get_response(method=self.METHOD, url=url, data=data,
                                      logger_message=f"Запрос на обновление access-токена "
                                                     f"по параметрам:{data}")
        return response


access_token = TokenManager(post_request_manager=RequestsPost(access_token=os.getenv('TOKEN'))).get_access_token()
request_manager = RequestsManager(access_token=access_token)
