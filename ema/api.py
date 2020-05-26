from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from ema.models import Event, SignUp
from ema.serializers import *


# Helpers

class Helper(object):
    def get_event(self, event_id):
        try:
            model = Event.objects.get(pk=event_id)
            return None, model
        except Event.DoesNotExist:
            response = Response('Event with id {} is not found'.format(event_id), status=status.HTTP_404_NOT_FOUND)
            return response, None

    def get_signup(self, event_id, signup_id):
        not_found_response, event = self.get_event(event_id)
        if None is event:
            return not_found_response

        try:
            signup = event.signups.get(pk=signup_id)
            return None, signup
        except SignUp.DoesNotExit:
            response = Response('Email id {} is not signed up to Event {}'.format(signup_id, event),
                                status=status.HTTP_404_NOT_FOUND)
            return response, None


# APIs

class EventList(APIView):
    def get(self, request):
        model = Event.objects.all()
        serializer = EventSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetails(APIView):
    def get(self, request, event_id):
        not_found_response, model = Helper().get_event(event_id)
        if None is model:
            return not_found_response
        serializer = EventSerializer(model)
        return Response(serializer.data)


class EventSignup(APIView):
    def get(self, request, event_id):
        not_found_response, event = Helper().get_event(event_id)
        if None is event:
            return not_found_response
        serializer = SignUpSerializer(event.signups.all(), many=True)
        return Response(serializer.data)

    def post(self, request, event_id):
        not_found_response, event = self.get_event(event_id)
        if None is event:
            return not_found_response

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        try:
            model = SignUp(event=event, email=user.email)
            model.save()
            serializer = SignUpSerializer(model)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                'Email {} is already signed up to Event with id {}',
                status=status.HTTP_400_BAD_REQUEST
            )


class SignUpDetails(APIView):
    def get(self, request, event_id, signup_id):
        not_found_response, signup = Helper().get_signup(event_id, signup_id)
        if None is signup:
            return not_found_response
        serializer = SignUpSerializer(signup)
        return Response(serializer.data)

    def delete(self, request, event_id, signup_id):
        not_found_response, signup = Helper().get_signup(event_id, signup_id)
        if None is signup:
            return not_found_response

        signup.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
