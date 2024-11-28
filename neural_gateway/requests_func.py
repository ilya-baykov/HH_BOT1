import time
import backoff
import requests
from typing import Optional

import urllib3

# Отключаем предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: e.response is not None and e.response.status_code < 400
)
def get_request(url: str, header: Optional[str] = None) -> requests.Response:
    """
        Отправка GET запроса

        Args:
            url (str): Ссылка

        Returns:
            requests.Response: Ответ с сервера
            :param url: url
            :param header: header
    """

    try:
        if not header:
            page = requests.get(url, verify=False, timeout=1 * 60)
        else:
            page = requests.get(url, verify=False, timeout=1 * 60, headers=header)
    except Exception:
        time.sleep(60)
        raise requests.exceptions.RequestException
    return page


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: e.response is not None and e.response.status_code < 400
)
def post_request(url: str, header: dict, data: dict | str) -> requests.Response:
    """
        Отправка POST запроса

        Args:
            url (str): Ссылка
            header (dict): Заголовок
            data (dict): Передаваемые параметры

        Returns:
            requests.Response: Ответ с сервера
    """

    try:
        response = requests.post(
            url, headers=header, data=data, verify=False, timeout=1 * 60
        )
    except Exception:
        time.sleep(60)
        raise requests.exceptions.RequestException
    return response
