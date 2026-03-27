from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    wiremock_host: str = Field(default="localhost:8094", alias="WIREMOCK_HOST", description="Wiremock host")
    currency_service_host: str = Field(default="localhost:8092", alias="CURRENCY_SERVICE_HOST", description="The service host")