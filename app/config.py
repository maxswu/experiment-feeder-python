from pydantic_settings import BaseSettings, SettingsConfigDict

from infra.market_info.service.config import TwseApiSettings


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )

    twse_api: TwseApiSettings = TwseApiSettings()


app_settings = AppSettings()
