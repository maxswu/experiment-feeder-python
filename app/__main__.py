import time
from argparse import ArgumentParser

import schedule

from app.config import app_settings
from app.task import get_twse_market_info_use_case

schedule.every(app_settings.task_interval_seconds).seconds.do(
    get_twse_market_info_use_case().get_security_info, app_settings.twse_targets
)


def run_pending():
    while True:
        idle_seconds = schedule.idle_seconds()
        if idle_seconds is None:
            break
        elif idle_seconds > 0:
            time.sleep(idle_seconds)
        schedule.run_pending()


parser = ArgumentParser()
parser.add_argument('-n', '--now', action='store_true')
args = parser.parse_args()

if args.now:
    schedule.run_all()
else:
    run_pending()
