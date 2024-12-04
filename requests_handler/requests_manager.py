import os
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
    def __init__(self, TOKEN: str):
        self.get = RequestsGet(TOKEN)
        self.post = RequestsPost(TOKEN)


class RequestsBase:
    BASE_URL = HH_BASE_URL

    def __init__(self, token: str):
        self._token = token

    @staticmethod
    def _get_response(method: str, url: str, data: Optional[dict] = None,
                      headers: Optional[dict] = None, logger_message: str = "") -> Optional[Response]:
        headers = headers if isinstance(headers, dict) else {}
        data = data if isinstance(data, dict) else {}

        if method.lower() == 'post':
            response = requests.post(url=url, headers=headers, data=data, verify=False)
        else:  # По умолчанию используем GET
            response = requests.get(url=url, headers=headers, data=data)

        try:
            response.raise_for_status()  # Проверяем статус ответа
            logger.info(f"{logger_message}. Статус - {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"{logger_message}.Произошла ошибка: {e}")
            return None


class RequestsGet(RequestsBase):
    METHOD = "GET"


class RequestsPost(RequestsBase):
    METHOD = "POST"

    def get_access_token(self, client_id: str, client_secret: str) -> Optional[Response]:
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
        params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
        url = f"{self.BASE_URL}/token"
        response = self._get_response(method=self.METHOD, url=url, data=params,
                                      logger_message=f"Запрос на получение access-токена "
                                                     f"по параметрам:{params}")
        return response


# Загружаем переменные окружения из файла .env
dotenv_path = r'C:\Users\ilyab\PycharmProjects\HH_BOT_1\requests_handler\.env'
try:
    load_dotenv(dotenv_path=dotenv_path)
except Exception as e:
    logger.error(f"При попытке загрузить файл:{dotenv_path} произошла ошибка - {e}")
    raise EnvFileLoadError(f"Не удалось загрузить файл: {dotenv_path}") from e

__TOKEN = os.getenv('TOKEN')
if __TOKEN is None:
    raise TokenNotFoundError("Токен не найден. Убедитесь, что переменная 'TOKEN' определена в .env файле.")

otrs_request_manager = RequestsManager(TOKEN=__TOKEN)
otrs_request_manager.post.get_access_token(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
