from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    auth_url: str
    niffler_username: str
    niffler_password: str
    gateway_url: str
    spend_db_url: str
    kafka_address: str
    userdata_db_url: str
    soap_url: str