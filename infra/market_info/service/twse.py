from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
import httpx
from loguru import logger
from typing import Collection, override

from domain.market_info.model.twse import TwseSecurityInfo
from domain.market_info.service.twse import ITwseMarketInfoService
from infra.market_info.service.config import TwseApiSettings

TWSE_TZ = ZoneInfo('Asia/Taipei')


class StockInfoResponseEntity(BaseModel):
    """
    API response model for TWSE official API
    """

    code: str = Field(..., title='代碼', validation_alias='c')
    name: str = Field(..., title='簡稱', validation_alias='n')
    full_name: str = Field(..., title='全名', validation_alias='nf')
    opening_price: Decimal | str = Field(..., title='開盤價', validation_alias='o')
    current_intraday_price: Decimal | str = Field(
        ..., title='當前盤中成交價', validation_alias='z'
    )
    highest_price: Decimal | str = Field(..., title='最高價', validation_alias='h')
    lowest_price: Decimal | str = Field(..., title='最低價', validation_alias='l')
    updated_time_ms: int = Field(
        ..., title='資料更新時間(毫秒)', validation_alias='tlong'
    )

    def to_domain_model(self, query_time: float) -> TwseSecurityInfo | None:
        """
        Convert entity to domain model
        :param query_time: in timestamp
        :return: `TwseSecurityInfo`
        """

        # Price values maybe '-' due to source API
        if (
            self.opening_price == '-'
            or self.current_intraday_price == '-'
            or self.highest_price == '-'
            or self.lowest_price == '-'
        ):
            logger.debug(f'No available prices for {self.code}')
            return None

        return TwseSecurityInfo(
            **self.model_dump(by_alias=False),
            updated_time=self.updated_time_ms / 1000,
            query_time=query_time,
        )


class StockInfoResponseQueryTime(BaseModel):
    """
    API response model for TWSE official API
    """

    sys_date: str = Field(..., validation_alias='sysDate')
    sys_time: str = Field(..., validation_alias='sysTime')

    @property
    def query_time(self) -> float:
        """
        Convert query time response to timestamp
        :return: timestamp in `float`
        """
        return (
            datetime.strptime(f'{self.sys_date}{self.sys_time}', '%Y%m%d%H:%M:%S')
            .replace(tzinfo=TWSE_TZ)
            .timestamp()
        )


class StockInfoResponse(BaseModel):
    """
    API response model for TWSE official API
    """

    msg_array: list[StockInfoResponseEntity] = Field(..., validation_alias='msgArray')
    query_time: StockInfoResponseQueryTime = Field(..., validation_alias='queryTime')

    def to_domain_models(self) -> list[TwseSecurityInfo]:
        results = []
        for e in self.msg_array:
            m = e.to_domain_model(self.query_time.query_time)
            if m is not None:
                results.append(m)
        return results


class TwseApiMarketInfoService(ITwseMarketInfoService):
    """
    TWSE market info service backed by official API
    """

    def __init__(self, settings: TwseApiSettings):
        self.settings = settings

    @override
    async def get_security_info(
        self, code: str | Collection[str]
    ) -> list[TwseSecurityInfo]:
        code_str = code if isinstance(code, str) else '|'.join(code)
        logger.debug(f'Getting {code} from TWSE API')
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                url=f'{self.settings.api_root}{self.settings.stock_info_path}',
                params=dict(
                    json=1,
                    delay=0,
                    ex_ch=code_str,
                ),
                timeout=self.settings.timeout_seconds,
            )
            resp_model = StockInfoResponse.model_validate_json(resp.content)
            return resp_model.to_domain_models()
