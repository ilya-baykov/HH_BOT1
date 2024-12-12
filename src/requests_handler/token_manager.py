import json
import os
from datetime import datetime, timedelta

from requests import Response

from config.constants.paths import ACCESS_TOKEN_JSON_PATH
from config.logger import logger


class TokenManager:
    """ Менеджер токенов для управления доступом к API. """

    def __init__(self, post_request_manager, access_token_path=ACCESS_TOKEN_JSON_PATH):
        """
        Инициализация TokenManager.

        Args:
            post_request_manager (RequestsPost): Менеджер для выполнения POST-запросов.
            access_token_path (str): Путь к файлу с токенами (по умолчанию 'ACCESS_TOKEN_JSON_PATH').
        """
        self.access_token_path = access_token_path
        self.post_request_manager = post_request_manager  # RequestsPost
        self.json_data = self._load_tokens()

    def _load_tokens(self) -> dict:
        """ Загружает токены из файла. """
        with open(self.access_token_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _save_tokens(self, tokens: dict) -> None:
        """ Сохраняет токены в файл. """
        with open(self.access_token_path, 'w', encoding='utf-8') as json_file:
            json.dump(tokens, json_file, indent=4)

    def _is_token_expired(self) -> bool:
        """Проверяет, истек ли срок действия токена."""
        creation_date = datetime.fromtimestamp(os.path.getctime(self.access_token_path))
        return datetime.now() > creation_date + timedelta(days=14)

    def _update_access_token_if_needed(self) -> None:
        """Обновляет токен доступа, если он истек."""
        if self._is_token_expired():
            update_tokens: Response = self.post_request_manager.update_user_access_token(
                refresh_token=self.json_data.get('refresh_token'))

            if update_tokens and update_tokens.status_code == 200:
                self.json_data.update(update_tokens.json())
                self._save_tokens(self.json_data)
            else:
                logger.error("Не удалось обновить токен.")

    def get_access_token(self) -> str:
        """Получает токен доступа, обновляя его при необходимости."""
        self._update_access_token_if_needed()
        return self.json_data.get('access_token')
