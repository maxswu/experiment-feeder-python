from loguru import logger
from typing import override

from domain.market_info.repository.asset_info import IAssetInfoRepository, AssetInfoT


class LoggerAssetInfoRepository(IAssetInfoRepository):
    @override
    def save_asset_info(self, asset_info: AssetInfoT) -> None:
        logger.debug(f'Saving {asset_info}')
