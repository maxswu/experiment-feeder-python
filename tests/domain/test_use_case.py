from unittest.mock import AsyncMock

import pytest

from polyfactory.factories.pydantic_factory import ModelFactory

from domain.market_info.model.twse import TwseSecurityInfo
from domain.market_info.repository.asset_info import IAssetInfoRepository
from domain.market_info.service.twse import ITwseMarketInfoService
from domain.market_info.use_case import TwseMarketInfoUseCase


@pytest.fixture
def mock_repository():
    mock_repo = AsyncMock(spec=IAssetInfoRepository)
    yield mock_repo


@pytest.fixture
def mock_service():
    mock_service = AsyncMock(spec=ITwseMarketInfoService)
    yield mock_service


class TwseSecurityInfoFactory(ModelFactory[TwseSecurityInfo]):
    """
    Mock model factory powered by polyfactory
    """


@pytest.fixture
def mock_security_info():
    yield TwseSecurityInfoFactory.build()


class TestTwseMarketInfoUseCase:

    @pytest.fixture(autouse=True)
    def setup(self, mock_service, mock_repository):
        self.mock_service = mock_service
        self.mock_repository = mock_repository
        self.use_case = TwseMarketInfoUseCase(
            twse_market_info_service=self.mock_service,
            asset_info_repository=self.mock_repository,
        )
        yield

    async def test_get_security_info__single(self, mock_security_info):
        self.mock_service.get_security_info.return_value = [mock_security_info]

        results = await self.use_case.get_security_info(code=mock_security_info.code)

        assert isinstance(results, list)
        assert len(results) == 1
        assert isinstance(results[0], TwseSecurityInfo)
        self.mock_service.get_security_info.assert_awaited_once()
        self.mock_repository.save_asset_info.assert_awaited_once()
