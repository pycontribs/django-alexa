from __future__ import absolute_import
from django.conf.urls import url, include
from rest_framework import routers
from .views import ASKViewSet

router = routers.DefaultRouter()
router.register(r"ask", ASKViewSet, base_name="ask")
router.include_root_view = False

urlpatterns = [
    url(r'^alexa/', include(router.urls), name="alexa"),
]
