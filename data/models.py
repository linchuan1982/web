#coding=utf-8
from enum import Enum
from django.db import models
from analysis.models import Source, SearchUrl

# Create your models here.
class FileType(Enum):
    video = 0
    audio = 1


class ExtraAsset(models.Model):
    title = models.CharField(max_length=300, default='', null=True, blank=True)
    link_url = models.ManyToManyField(SearchUrl)
    media_url = models.CharField(default='', max_length=1024, blank=True)
    asset_key = models.CharField(default='', max_length=80, null=False, blank=False, db_index=True)
    source = models.SmallIntegerField(null=False, blank=False, choices=[(tag.value, tag.name) for tag in Source])
    asset_type = models.SmallIntegerField(null=False, blank=False, choices=[(tag.value, tag.name) for tag in FileType])
    # 是否下载已完成
    in_lib = models.BooleanField(default=False, null=False, blank=False)
    # visible 是否可见
    inlib_time = models.DateTimeField(null=True, blank=True)
    # 如果多次查询网址存在这个视频，则刷新update, 表示该视频一直处于热门状态
    update_at = models.DateField(null=True, blank=True)
