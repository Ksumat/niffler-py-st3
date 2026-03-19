import allure
from resources.templates.read_templates import current_user_xml
from tools.soap_helper import parsed_result


@allure.feature('Профиль пользователя')
@allure.story('SOAP')
class TestSoap:
    @allure.title('SOAP: Получение информации о пользователе')
    def test_current_user_info_by_soap(self, soap_session, envs):
        response = soap_session.request('POST', '', data=current_user_xml(envs.niffler_username))
        assert response.status_code == 200

        user_data = parsed_result(response.text)

        assert user_data['username'] == envs.niffler_username
        assert user_data['currency'] == 'RUB'
