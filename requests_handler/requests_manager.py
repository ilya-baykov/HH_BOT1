import os
import urllib

import requests
import urllib3
from typing import Optional
from dotenv import load_dotenv
from requests import Response

from logger import logger

from requests_handler.constants.base_url import HH_BASE_URL
from requests_handler.exceptions import EnvFileLoadError, TokenNotFoundError

# Отключаем предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RequestsManager:
    def __init__(self, ACCESS_TOKEN: str):
        if ACCESS_TOKEN is None:
            raise TokenNotFoundError("Токен не найден. Убедитесь, что переменная 'TOKEN' определена в .env файле.")

        self.get = RequestsGet(ACCESS_TOKEN)
        self.post = RequestsPost(ACCESS_TOKEN)
        self.reference_book_get = ReferenceBookRequestsGet(ACCESS_TOKEN)


class RequestsBase:
    BASE_URL = HH_BASE_URL

    def __init__(self, ACCESS_TOKEN: str):
        self.headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
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
            logger.info(f"{logger_message}. Статус - {response.status_code}")
            response_url = response.url
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

    def get_access_token_user(self, client_id: str, client_secret: str, code: str,
                              redirect_uri: str) -> Optional[Response]:
        data = {'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'}

        url = f"{self.BASE_URL}/token"
        response = self._get_response(method=self.METHOD, url=url, data=data,
                                      logger_message=f"Запрос на получение access-токена "
                                                     f"по параметрам:{data}")
        return response


# Загружаем переменные окружения из файла .env
dotenv_path = r'C:\Users\ilyab\PycharmProjects\HH_BOT_1\requests_handler\.env'
try:
    load_dotenv(dotenv_path=dotenv_path)
except Exception as e:
    logger.error(f"При попытке загрузить файл:{dotenv_path} произошла ошибка - {e}")
    raise EnvFileLoadError(f"Не удалось загрузить файл: {dotenv_path}") from e

request_manager = RequestsManager(
    ACCESS_TOKEN='USERG50OSH6FBK6BBRQP5SHP6P47BPN4C0IK2739NTF9BGN163OGNOFIN1N6CIPE')
