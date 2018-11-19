# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from django.db import models

# Create your models here.
# 发表会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateField('events_time')
    create_time = models.DateField(auto_now=True)
    sign_in = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event)
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('event','phone')

    def __str__(self):
        return self.realname