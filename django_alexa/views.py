from __future__ import absolute_import
import logging
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from . import serializers
from .api import validation


log = logging.getLogger(__name__)


class ASKViewSet(GenericViewSet):
    serializer_class = serializers.ASKSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            log.exception("Error occured during request serialization!")
            raise e
        serializer.save()
        response = Response(serializer.data, status=HTTP_200_OK)
        return response

    def dispatch(self, request, *args, **kwargs):
        validation.validate_alexa_request(request.META, request.body)
        response = super(ASKViewSet, self).dispatch(request, *args, **kwargs)
        validation.validate_reponse_limit(response.render().content)
        return response
