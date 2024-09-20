import json

from loguru import logger
from typing import override, Any

from confluent_kafka import Producer, KafkaError, Message
from domain.market_info.repository.asset_info import IAssetInfoRepository, AssetInfoT
from infra.config import KafkaSettings


class LoggerAssetInfoRepository(IAssetInfoRepository):
    @override
    async def save_asset_info(self, asset_info: AssetInfoT) -> None:
        logger.debug(f'Saving {asset_info}')


class KafkaAssetInfoRepository(IAssetInfoRepository):
    ASSET_INFO_TOPIC: str = 'asset.info.view.v1'

    def __init__(self, kafka_settings: KafkaSettings):
        self.kafka_settings = kafka_settings
        self.producer = Producer(self.kafka_settings.producer_config_dict)

    @staticmethod
    def _on_kafka_delivery(err: KafkaError | None, msg: Message | None) -> None:
        is_success: bool = err is None
        if is_success:
            if msg:
                logger.debug(
                    f'Message delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}'
                )
            else:
                logger.debug(
                    'Message delivered successfully, but no message was returned.'
                )
        else:
            logger.error(f'Message delivery failed: {err}')

    async def _produce_to_kafka(self, key: dict | None, value: dict):
        self.producer.produce(
            topic=self.ASSET_INFO_TOPIC,
            key=json.dumps(key) if key else None,
            value=json.dumps(value),
            on_delivery=self._on_kafka_delivery,
        )
        self.producer.flush()

    @override
    async def save_asset_info(self, asset_info: AssetInfoT) -> None:
        key: dict[str, str] = dict(code=asset_info.code)
        value: dict[str, Any] = asset_info.model_dump(mode='json')
        logger.debug(f'Producing {value}')
        await self._produce_to_kafka(key=key, value=value)
