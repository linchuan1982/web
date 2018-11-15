from django.db import models
from enum import Enum


class Source(Enum):   # A subclass of Enum
    youtube = 0
    twitter = 1
    unknown = 2


# Create your models here.
class SearchUrl(models.Model):
    request_url = models.CharField(default='', max_length=1024, null=False, blank=True, db_index=True)
    source = models.SmallIntegerField(null=False, blank=False, choices=[(tag.value, tag.name) for tag in Source])
    create_at = models.DateTimeField(auto_now_add=True)
    fetch_at = models.DateTimeField(null=True, blank=True)
