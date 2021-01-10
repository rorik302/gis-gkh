from django.db import models


class House(models.Model):
    fias_id = models.CharField(max_length=50, default='')
    guid = models.CharField(max_length=50, default='')
    passport_url = models.CharField(max_length=255, default='', null=True)
    passport_info = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
