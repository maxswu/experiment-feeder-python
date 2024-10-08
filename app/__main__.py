from argparse import ArgumentParser
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import app_settings
from app.job import get_twse_market_info_use_case


async def main():
    """
    Scheduled run
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=get_twse_market_info_use_case().get_security_info,
        trigger='cron',
        timezone='Asia/Taipei',
        day_of_week='mon-fri',
        hour='9-15',
        second=f'*/{app_settings.task_interval_seconds}',
        kwargs=dict(code=app_settings.twse_targets),
    )
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


async def dry_run():
    """
    Run once without saving to repositories
    """
    await get_twse_market_info_use_case(dry_run=True).get_security_info(
        code=app_settings.twse_targets
    )


parser = ArgumentParser()
parser.add_argument('-d', '--dry', action='store_true')
args = parser.parse_args()

try:
    if args.dry:
        asyncio.run(dry_run())
    else:
        asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    pass
