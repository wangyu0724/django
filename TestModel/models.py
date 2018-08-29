# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20)


class Contact(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
