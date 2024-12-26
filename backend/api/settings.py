from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


def get_model_config(env_prefix: str = "") -> SettingsConfigDict:
    return SettingsConfigDict(env_prefix=env_prefix, env_file=".env", extra="ignore")


class AppSettings(BaseSettings):
    name: str = "RateReel"
    version: str = "1.0.0"
    title: str = "RateReel"
    summary: str = "Rate movies and leave reviews"


class PostgresSettings(BaseSettings):
    host: str
    port: int
    password: str
    user: str
    db: str
    db_schema: str

    @property
    def connection_url(self) -> str:
        url = URL.create(
            "postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.db,
        )
        return url.render_as_string(hide_password=False)

    model_config = get_model_config("postgres_")


class JWTSettings(BaseSettings):
    secret_key: str

    model_config = get_model_config("jwt_")


app_settings = AppSettings()
postgres_settings = PostgresSettings()
jwt_settings = JWTSettings()
