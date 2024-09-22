from functools import lru_cache

from app.config import app_settings
from domain.market_info.use_case import TwseMarketInfoUseCase
from infra.market_info.repository.asset_info import (
    LoggerAssetInfoRepository,
    KafkaAssetInfoRepository,
)
from infra.market_info.service.twse import TwseApiMarketInfoService


@lru_cache
def get_twse_market_info_use_case(dry_run: bool = False) -> TwseMarketInfoUseCase:
    """
    Cached TWSE market info use case
    :param dry_run: if set to `True`, `LoggerAssetInfoRepository` will be used as repository
    :return: `TwseMarketInfoUseCase`
    """
    if dry_run:
        return TwseMarketInfoUseCase(
            twse_market_info_service=TwseApiMarketInfoService(
                settings=app_settings.twse_api
            ),
            asset_info_repository=LoggerAssetInfoRepository(),
        )
    else:
        return TwseMarketInfoUseCase(
            twse_market_info_service=TwseApiMarketInfoService(
                settings=app_settings.twse_api
            ),
            asset_info_repository=KafkaAssetInfoRepository(
                kafka_settings=app_settings.kafka
            ),
        )
