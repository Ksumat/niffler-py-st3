from typing import Any
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

namespace = {
    'ns2': 'niffler-userdata'
}


def _find_text(element: Element, tag: str, ns: dict[str, str]):
    el = element.find(tag, ns)
    return el.text if el is not None else None


def parsed_result(xml_str: str) -> dict[str, Any]:
    root = ElementTree.fromstring(xml_str)
    user = root.find('.//ns2:user', namespace)
    user_data = {
        'username': _find_text(user, 'ns2:username', namespace),
        'currency': _find_text(user, 'ns2:currency', namespace),
        'friendshipStatus': _find_text(user, 'ns2:friendshipStatus', namespace)
    }
    return user_data
