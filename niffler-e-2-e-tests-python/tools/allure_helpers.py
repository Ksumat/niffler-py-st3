import json
import logging
from json import JSONDecodeError

import allure
import curlify
from allure_commons.types import AttachmentType
from requests import Response
from jinja2 import Environment, PackageLoader, select_autoescape


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""

    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        env = Environment(
            loader=PackageLoader("resources"),
            autoescape=select_autoescape()
        )
        request_template = env.get_template("http-colored-request.ftl")
        response_template = env.get_template("http-colored-response.ftl")

        with allure.step(f"{method} {url}"):

            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)
            try:
                prepare_request_render = {
                    "request": response.request,
                    "curl": curl,
                }
                request_render = request_template.render(prepare_request_render)

                prepare_response_render = {
                    "response": response
                }
                response_render = response_template.render(prepare_response_render)
            except Exception as e:
                logging.error(f"Не смогли срендерить шаблон для отчета: {e}")
                request_render = f"CURL: {curl}\nURL: {response.request.url}"
                response_render = f"Status: {response.status_code}\nBody: {response.text[:500]}..."

            allure.attach(
                body=request_render,
                name="Request",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
            allure.attach(
                body=response_render.encode('utf-8'),
                name=f"Response {response.status_code}",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".html"
                )
            except (JSONDecodeError, TypeError):
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")
        return response

    return wrapper


def attach_sql(coursor, statement, parameters, context):
    """Прикрепляет SQL запрос в аллюре"""

    statement_with_params = statement % parameters
    name = statement.split(" ")[0] + " " + context.engine.url.database
    allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)