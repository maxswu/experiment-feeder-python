import abc
from abc import abstractmethod
from collections.abc import Collection

from domain.market_info.model.twse import TwseSecurityInfo


class ITwseMarketInfoService(abc.ABC):
    """
    Abstract service class for TWSE market info
    """

    @abstractmethod
    async def get_security_info(
        self, code: str | Collection[str]
    ) -> list[TwseSecurityInfo]:
        """
        Get security info (can be multiple)
        :param code:
        :return: `list` of `TwseSecurityInfo`
        """
