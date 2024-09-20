import abc
from typing import TypeVar

from domain.market_info.model.common import AssetInfo

AssetInfoT = TypeVar('AssetInfoT', bound=AssetInfo)


class IAssetInfoRepository(abc.ABC):
    @abc.abstractmethod
    async def save_asset_info(self, asset_info: AssetInfoT) -> None:
        """
        Save to repository
        :param asset_info:
        :return:
        """
