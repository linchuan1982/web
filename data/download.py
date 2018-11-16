#coding=utf-8
import subprocess
from datetime import datetime
from data.models import ExtraAsset, DownloadStatus

from celery import task, shared_task

import logging

logger = logging.getLogger()


@task
def check_assets():
    eas = ExtraAsset.objects.filter(status__in=[DownloadStatus.faield.value, DownloadStatus.initial.value])
    for ea in eas:
        download_asset.delay(ea.asset_key)


@shared_task
def download_asset(asset_key):
    ea = ExtraAsset.objects.get(asset_key=asset_key)
    ea.status = DownloadStatus.started.value
    ea.save()
    cmd = ['youtube-dl', '--proxy', 'socks5://127.0.0.1:1086', ea.media_url]
    try:
        out_bytes = subprocess.check_output(
            cmd, cwd='/data/lib')
    except subprocess.CalledProcessError as e:
        out_bytes = e.output       # Output generated before error
        code      = e.returncode   # Return code
        logger.error('download failed, url={url} err_code={code} msg={err_msg}'.format(url=ea.media_url, code=code, err_msg=out_bytes))
        ea.status = DownloadStatus.faield.value
        ea.save()
        return
    else:
        ea.status = DownloadStatus.finished.value
        ea.inlib_time = datetime.now()
        ea.save()
    return
