from __future__ import absolute_import
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from . import serializers
from .api import validation


class ASKViewSet(GenericViewSet):
    serializer_class = serializers.ASKSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=HTTP_200_OK)
        validation.validate_reponse_limit(response)
        return response

    def dispatch(self, request, *args, **kwargs):
        validation.validate_alexa_request(request)
        return super(ASKViewSet, self).dispatch(request, *args, **kwargs)
