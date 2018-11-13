import json
from urllib import parse
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, HttpResponseBadRequest
from .youtube import get_links
from analysis.models import SearchUrl, Source
import logging

logger = logging.getLogger(__name__)


def index(request):
    # print(request)
    url = request.GET.get('url', None)

    host = parse.splithost(parse.splittype(url)[1])[0]
    logger.info('host is {}'.format(host))
    source = None
    for tag in Source:
        if tag.name in host:
            source = tag.value
            break
    if source is None:
        return HttpResponseBadRequest('Unknown url {}'.format(url))

    # 更新数据库
    item, create_ = SearchUrl.objects.get_or_create(
        request_url=url, defaults=dict(source=source)
    )
    return HttpResponse('ok')
