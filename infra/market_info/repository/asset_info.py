import json

from loguru import logger
from typing import override, Any

from confluent_kafka import Producer, KafkaError, Message

from domain.market_info.model.twse import TwseSecurityInfo
from domain.market_info.repository.asset_info import IAssetInfoRepository, AssetInfoT
from infra.config import KafkaSettings


class LoggerAssetInfoRepository(IAssetInfoRepository):
    """
    A simple `IAssetInfoRepository` implementation that logs `AssetInfo` only
    """

    @override
    async def save_asset_info(self, asset_info: AssetInfoT) -> AssetInfoT:
        logger.debug(f'Saving {asset_info}')
        return asset_info


class KafkaAssetInfoRepository(IAssetInfoRepository):
    """
    Asset info repository backed by Kafka topic
    """

    ASSET_INFO_TOPIC: str = 'asset.info.view.v1'

    def __init__(self, kafka_settings: KafkaSettings):
        self.kafka_settings = kafka_settings
        self.producer = Producer(self.kafka_settings.producer_config_dict)

    @staticmethod
    def _on_kafka_delivery(err: KafkaError | None, msg: Message | None) -> None:
        """
        Callback function for Kafka producer after delivery
        :param err: `KafkaError` if something goes wrong with Kafka
        :param msg: `Message` if delivered
        """
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

    async def _produce_to_kafka(self, key: dict | None, value: dict) -> None:
        """
        Produce to Kafka in json format
        :param key:
        :param value:
        """
        self.producer.produce(
            topic=self.ASSET_INFO_TOPIC,
            key=json.dumps(key) if key else None,
            value=json.dumps(value),
            on_delivery=self._on_kafka_delivery,
        )
        self.producer.flush()

    @override
    async def save_asset_info(self, asset_info: TwseSecurityInfo) -> TwseSecurityInfo:
        key: dict[str, str] = dict(code=asset_info.code)
        value: dict[str, Any] = asset_info.model_dump(mode='json')
        logger.debug(f'Producing {value}')
        await self._produce_to_kafka(key=key, value=value)
        return asset_info
