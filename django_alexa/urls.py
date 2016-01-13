from __future__ import absolute_import
from django.conf.urls import url, include
from rest_framework import routers
from .views import ASKView

urlpatterns = [
    url(r'^alexa/ask/$', ASKView.as_view(), name="alexa"),
]
