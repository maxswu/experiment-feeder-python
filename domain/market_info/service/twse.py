import abc
from abc import abstractmethod
from collections.abc import Collection

from domain.market_info.model.twse import TwseSecurityInfo


class ITwseMarketInfoService(abc.ABC):
    @abstractmethod
    def get_security_info(self, code: str | Collection[str]) -> list[TwseSecurityInfo]:
        pass
