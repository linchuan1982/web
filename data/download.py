#coding=utf-8
import subprocess
from datetime import datetime
from data.models import ExtraAsset

from celery import shared_task
from timer_tasks.celery_timer_config import timer_task
from extract.celery import async_app

import logging

logger = logging.getLogger()


@timer_task.task
def check_assets():
    eas = ExtraAsset.objects.filter(in_lib=False)
    for ea in eas:
        download_asset.delay(ea.asset_key)


@shared_task
def download_asset(asset_key):
    ea = ExtraAsset.ojbects.get(asset_key)
    cmd = ['youtube-dl', '--proxy', 'socks5://127.0.0.1:1086', ea.media_url]
    try:
        out_bytes = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        out_bytes = e.output       # Output generated before error
        code      = e.returncode   # Return code
        logger.error('download failed, url={url} err_code={code} msg={err_msg}'.format(url=ea.media_url, code=code, err_msg=out_bytes))
        return
    else:
        ea.in_lib = True
        ea.inlib_time = datetime.now()
        ea.save()
    return
