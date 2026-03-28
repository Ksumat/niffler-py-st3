import os
import grpc
import pytest

from database.userdata_db import UserdataDb
from models.config import Envs
from dotenv import load_dotenv
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from clients.kafka_client import KafkaClient
from tools.sessions import SoapSession
#from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
#from internal.pb.grpc.interceptors.allure import AllureInterceptor
#from internal.pb.grpc.interceptors.logging import LoggingInterceptor
#from settings.settings import Settings

INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                auth_url=os.getenv("AUTH_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD'),
                gateway_url=os.getenv('GATEWAY_URL'),
                spend_db_url=os.getenv("SPEND_DB_URL"),
                kafka_address=os.getenv("KAFKA_ADDRESS"),
                userdata_db_url=os.getenv("USER_DB_URL"),
                soap_url=os.getenv("SOAP_URL"),
                grpc_port=os.getenv("GRPC_PORT")
                )


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.fixture(scope="session")
def kafka(envs: Envs):
    """Взаимодействие с Kafka"""
    with KafkaClient(envs) as k:
        yield k


@pytest.fixture(scope="session")
def user_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)


@pytest.fixture(scope='module')
def soap_session(envs):
    session = SoapSession(soap_url=envs.soap_url)
    return session


@pytest.fixture(scope="session", autouse=True)
def create_test_user_before_run(auth_client, envs):
    try:
        auth_client.register(username=envs.niffler_username, password=envs.niffler_password)
    except Exception as err:
        print(f"User exists: {err}")


#@pytest.fixture(scope="session")
#def settings() -> Settings:
    #""" Fixture for settings """
    #return Settings()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--mock", action="store_true", default=False)
