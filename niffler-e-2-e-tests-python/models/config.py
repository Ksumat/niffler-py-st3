from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    auth_url: str
    niffler_username: str
    niffler_password: str
    gateway_url: str