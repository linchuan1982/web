from celery import shared_task
from .youtube import get_links
import logging
import subprocess
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


@shared_task
def try_task(url):
    summ = get_links(url)
    for _ in summ:
        download_url.delay(urljoin('https://www.youtube.com/', _['url']))
    return


@shared_task
def download_url(url):
    cmd = ['youtube-dl', '--proxy', 'socks5://127.0.0.1:1086', url]
    pipe = subprocess.Popen(cmd)
    out, err = pipe.communicate()

