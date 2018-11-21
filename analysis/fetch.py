import json
from analysis.youtube import get_links
from analysis.models import SearchUrl
from data.models import ExtraAsset, FileType, DownloadStatus
from celery import shared_task, task
from async_task.celery_config import async_task
from timer_task.celery_config import timer_task
from datetime import datetime


@async_task.task
def fetch_all():
    urls = SearchUrl.objects.all()
    for url in urls:
        url.fetch_at = datetime.now()
        url.save()
        fetch_one_link.delay(url.request_url, url.source)

@shared_task
def fetch_one_link(url, source):
    summ = get_links(url)
    asset_keys = [_['asset_key'] for _ in summ]
    exist_keys = ExtraAsset.objects.filter(asset_key__in=asset_keys).values_list('asset_key', flat=True)
    for item in summ:
        if item['asset_key'] in exist_keys:
            continue

        su = SearchUrl.objects.get(request_url=url)

        ex = ExtraAsset.objects.create(
            title=item['title'],
            media_url=item['url'],
            asset_key=item['asset_key'],
            source=source,
            asset_type=FileType.video.value,
            status=DownloadStatus.initial.value,
        )
        ex.link_url.add(su)
        ex.save()
