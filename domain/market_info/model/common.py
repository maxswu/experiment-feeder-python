import abc

from pydantic import BaseModel, Field


class AssetInfo(BaseModel, abc.ABC):
    exchange: str = Field(..., title='市場別(交易所)')
    code: str = Field(..., title='代號')
    name: str = Field(..., title='名稱')
    query_time: float = Field(..., title='查詢時間')
