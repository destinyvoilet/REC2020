#coding=utf-8
from django.urls import path
from . import app1,app2_use
urlpatterns = [
    path(r'^app1$', app1.application1(aa,bb,cc)),
    path(r'^app2$', app2_use.application2(string)),
]
