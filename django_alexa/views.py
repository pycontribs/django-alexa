from __future__ import absolute_import
import logging
import traceback
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from .serializers import ASKInputSerializer
from .api import ResponseBuilder, IntentsSchema, InternalError, validate_alexa_request, validate_reponse_limit


log = logging.getLogger(__name__)


class ASKView(APIView):

    def handle_exception(self, exc):
        if settings.DEBUG:
            log.exception("An error occured in your skill.")
            msg = "An error occured in your skill.  Please check the response card for details."
            title = exc.__class__.__name__
            content = traceback.format_exc()
            data = ResponseBuilder.create_response(message=msg,
                                                   title=title,
                                                   content=content)
        else:
            msg = "An internal error occured in the skill."
            log.exception(msg)
            data = ResponseBuilder.create_response(message=msg)
        return Response(data=data, status=HTTP_200_OK)


    def handle_request(self, validated_data):
        log.info("Alexa Request Body: {0}".format(validated_data))
        intent_kwargs = {}
        session = validated_data['session']
        if validated_data["request"]["type"] == "IntentRequest":
            intent_name = validated_data["request"]["intent"]["name"]
            for slot, slot_data in validated_data["request"]["intent"].get("slots", {}).items():
                slot_key = slot_data["name"]
                try:
                    slot_value = slot_data['value']
                except KeyError as e:
                    msg = "Slot {0} had not value given".format(slot_key)
                    raise InternalError(msg)
                intent_kwargs[slot_key] = slot_value
        else:
            intent_name = validated_data["request"]["type"]
        data = IntentsSchema.route(intent_name, session, intent_kwargs)
        return Response(data=data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # we have to save the request body because we need to set the version
        # before we do anything dangerous so that we can properly send exception
        # reponses and the DRF request object doesn't allow you to access the
        # body after you have accessed the "data" stream
        body = request.body
        ResponseBuilder.set_version(request.data['version'])
        validate_alexa_request(request.META, body)
        serializer = ASKInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.handle_request(serializer.validated_data)

    def dispatch(self, request, *args, **kwargs):
        log.debug("#"*10+"Start Alexa Request"+"#"*10)
        response = super(ASKView, self).dispatch(request, *args, **kwargs)
        validate_reponse_limit(response.render().content)
        log.debug("#"*10+"End Alexa Request"+"#"*10)
        return response
