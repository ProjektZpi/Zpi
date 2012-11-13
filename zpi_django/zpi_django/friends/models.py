#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class FriendList(models.Model):
    user = models.ForeignKey(User)
    friend = models.ForeignKey(User, related_name="friend")
    confirmed = models.BooleanField()