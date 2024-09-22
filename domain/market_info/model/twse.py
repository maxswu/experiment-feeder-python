from pydantic import Field
from decimal import Decimal

from domain.market_info.model.common import AssetInfo


class TwseSecurityInfo(AssetInfo):
    """
    Asset info model class for TWSE securities only
    """

    exchange: str = 'TWSE'
    full_name: str = Field(..., title='全名')
    opening_price: Decimal = Field(..., title='開盤價')
    current_intraday_price: Decimal = Field(..., title='當前盤中成交價')
    highest_price: Decimal = Field(..., title='最高價')
    lowest_price: Decimal = Field(..., title='最低價')
    updated_time: float = Field(..., title='資料更新時間')
