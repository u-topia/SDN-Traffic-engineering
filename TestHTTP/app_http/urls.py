# -*- coding: UTF-8 -*-
from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    url(r"^hello/$", views.hello, name = "hello"),
    url(r"^show/$", views.showlinediagram),
]