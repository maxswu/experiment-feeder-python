import time

import schedule

from app.task import get_twse_market_info_use_case

schedule.every(1).minutes.do(
    get_twse_market_info_use_case().get_security_info, ['tse_2330.tw', 'otc_6021.tw']
)

while True:
    schedule.run_pending()
    time.sleep(1)