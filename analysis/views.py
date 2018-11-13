import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from .tasks import try_task


# Create your views here.
from django.http import HttpResponse
from .youtube import get_links


def index(request):
    # print(request)
    url = request.GET.get('url', None)
    summ = try_task.delay(url)
    return HttpResponse('ok')
