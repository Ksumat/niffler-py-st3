from urllib.parse import parse_qs, urlparse, urljoin

import requests
from requests import Session

from tools.allure_helpers import allure_attach_request


def raise_for_status(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                # Создаём новое исключение с дополнительной информацией
                raise requests.HTTPError(
                    f"{e}\nResponse body: {response.text}"
                ) from e
            raise  # Перебрасываем исходное исключение для других статусов
        return response

    return wrapper


class BaseSession(Session):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")

    @raise_for_status
    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Логирование запроса и вклейка base_url."""
        return super().request(method, self.base_url + url, **kwargs)


class AuthSession(Session):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа.
    + Автосохранение cookies внутри сессии из кааждого response и redirect response, и 'code'."""

    def __init__(self, *args, **kwargs):
        """
        Прокидываем base_url - url авторизации из энвов
        code - код авторизации из redirect_uri"""
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")
        self.code = None

    @raise_for_status
    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Сохраняем все cookies из redirect'a и сохраняем code авторизации из redirect_uri,
        И используем в дальнейшем в последующих запросах этой сессии."""
        response = super().request(method, self.base_url + url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)
            code = parse_qs(urlparse(r.headers.get("Location")).query).get("code", None)
            if code:
                self.code = code
        return response


class SoapSession(Session):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.soap_url = kwargs.pop("soap_url", None)
        self.headers.update({
            'Content-Type': 'text/xml; charset=utf-8'
        })

    @raise_for_status
    @allure_attach_request
    def request(self, method: str, path: str = '', **kwargs):
        return super().request(method, urljoin(str(self.soap_url), path), **kwargs)
