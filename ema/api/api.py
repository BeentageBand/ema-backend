from ema.api.dal import DAL
from ema.api.serializers import EventSerializer, UserSerializer, SignUpSerializer
from ema.email.confirmationemail import EventConfirmationEmail
from ema.models import Event, SignUp
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ema.email.emailhandler import EmailHandler

# APIs

class EventList(APIView):
    def get(self, request):
        model = Event.objects.all()
        serializer = EventSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventDetails(APIView):
    dal = DAL()

    def get(self, request, event_id):
        model = self.dal.get_event(event_id)
        serializer = EventSerializer(model)
        return Response(serializer.data)


class EventSignup(APIView):
    dal = DAL()

    def get(self, request, event_id):
        event = self.dal.get_event(event_id)
        serializer = SignUpSerializer(event.signups.all(), many=True)
        return Response(serializer.data)

    def post(self, request, event_id):
        event = self.dal.get_event(event_id)
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()
        signup = self.dal.set_signup(event, user)
        signup_serializer = SignUpSerializer(signup)

        event_confirmation = EventConfirmationEmail(from_email=user.email, to_email=user.email, event=event)
        email_handler = EmailHandler()
        email_handler.send_email(event_confirmation.get_message())

        return Response(signup_serializer.data, status=status.HTTP_201_CREATED)


class SignUpDetails(APIView):
    dal = DAL()

    def get(self, request, event_id, signup_id):
        signup = self.dal.get_signup(event_id, signup_id)
        serializer = SignUpSerializer(signup)
        return Response(serializer.data)

    def delete(self, request, event_id, signup_id):
        signup = self.dal.get_signup(event_id, signup_id)
        signup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
