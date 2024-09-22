from pydantic import BaseModel, Field


class TwseApiSettings(BaseModel):
    """
    TWSE official API settings
    """

    api_root: str = Field(default='https://mis.twse.com.tw/stock/api', title='API root')
    stock_info_path: str = Field(default='/getStockInfo.jsp', title='個股資訊路徑')
    timeout_seconds: int = Field(default=10, title='Timeout Seconds')
