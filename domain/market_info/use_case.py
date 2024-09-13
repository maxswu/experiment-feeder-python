from loguru import logger
from collections.abc import Collection

from domain.market_info.model.twse import TwseSecurityInfo
from domain.market_info.repository.asset_info import IAssetInfoRepository
from domain.market_info.service.twse import ITwseMarketInfoService


class TwseMarketInfoUseCase:
    def __init__(
        self,
        twse_market_info_service: ITwseMarketInfoService,
        asset_info_repository: IAssetInfoRepository,
    ):
        self.twse_market_info_service = twse_market_info_service
        self.asset_info_repository = asset_info_repository

    def _save_security_info(self, security_info: TwseSecurityInfo) -> None:
        self.asset_info_repository.save_asset_info(security_info)

    def get_security_info(self, code: str | Collection[str]) -> list[TwseSecurityInfo]:
        target_code_list: list[str] = [code] if isinstance(code, str) else code

        logger.info(f'Getting {code} info from TWSE')
        security_info_list = self.twse_market_info_service.get_security_info(
            target_code_list
        )

        for security_info in security_info_list:
            self.asset_info_repository.save_asset_info(security_info)

        return security_info_list
