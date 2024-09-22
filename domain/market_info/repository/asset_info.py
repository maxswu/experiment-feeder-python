import abc
from typing import TypeVar

from domain.market_info.model.common import AssetInfo

AssetInfoT = TypeVar('AssetInfoT', bound=AssetInfo)


class IAssetInfoRepository(abc.ABC):
    """
    Abstract repository class for asset info
    """

    @abc.abstractmethod
    async def save_asset_info(self, asset_info: AssetInfoT) -> AssetInfoT:
        """
        Save to repository
        :param asset_info: `AssetInfoT`
        :return: `None`
        """
