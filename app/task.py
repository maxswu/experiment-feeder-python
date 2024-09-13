from functools import lru_cache

from app.config import app_settings
from domain.market_info.use_case import TwseMarketInfoUseCase
from infra.market_info.repository.asset_info import LoggerAssetInfoRepository
from infra.market_info.service.twse import TwseApiMarketInfoService


@lru_cache
def get_twse_market_info_use_case() -> TwseMarketInfoUseCase:
    return TwseMarketInfoUseCase(
        twse_market_info_service=TwseApiMarketInfoService(settings=app_settings.twse_api),
        asset_info_repository=LoggerAssetInfoRepository(),
    )
