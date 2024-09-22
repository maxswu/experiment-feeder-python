from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from infra.config import KafkaSettings
from infra.market_info.service.config import TwseApiSettings


class AppSettings(BaseSettings):
    """
    Application settings
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        nested_model_default_partial_update=True,
        extra='ignore',
    )

    task_interval_seconds: int = Field(
        default=60, title='Execute tasks every X seconds'
    )

    twse_targets: list[str] = Field(..., title='Target assets')
    twse_api: TwseApiSettings = TwseApiSettings()
    kafka: KafkaSettings = KafkaSettings()


app_settings = AppSettings()
