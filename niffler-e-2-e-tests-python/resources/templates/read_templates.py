import os

import xmlschema
from jinja2 import Environment, select_autoescape, FileSystemLoader
from xmlschema import XMLSchema11

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def current_user_xml(username: str) -> str:
    template = env.get_template('./resources/templates/xml/current_user.xml')
    return template.render({'username': username})

