from ema.api.dal import DAL
from ema.api.permissions import IsAdminOrReadOnly
from ema.api.serializers import EventSerializer, SignUpSerializer, EventWithoutSignupsSerializer, UserRequestSerializer
from ema.email.confirmationemail import EventConfirmationEmail
from ema.email.emailhandler import EmailHandler
from ema.models import UserRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView


# APIs

class EventList(APIView):
    """
    get:
    Get all the events of all existing users
    post:
    Create a new event
    """
    dal = DAL()
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        model = self.dal.list_events()
        serializer = EventSerializer(model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventDetails(APIView):
    """
    get:
    Get Event Details from given Event Id
    """
    dal = DAL()
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, event_id):
        model = self.dal.get_event(event_id)
        serializer = EventSerializer(model)
        return Response(serializer.data)

    def delete(self, request, event_id):
        event = self.dal.get_event(event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventSignUp(APIView):
    """
    get:
    List all SignUps for a given Event Id
    post:
    Create a new SignUp for a given Event Id
    """
    dal = DAL()
    permission_classes = [IsAdminUser]

    def get(self, request, event_id):
        event = self.dal.get_event(event_id)
        serializer = SignUpSerializer(event.signups.all(), many=True)
        return Response(serializer.data)

    def post(self, request, event_id):
        event = self.dal.get_event(event_id)

        user_serializer = UserRequestSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_request = user_serializer.save()

        signup = self.dal.set_signup(event, user_request.email)
        signup_serializer = SignUpSerializer(signup)

        return Response(signup_serializer.data, status=status.HTTP_201_CREATED)


class SignUpDetails(APIView):
    """
    get:
    Get Signup Details for given Event Id and SignUp Id
    delete:
    Destroy Signup Details for given Event Id and SignUp Id
    """
    dal = DAL()
    permission_classes = [IsAdminUser]

    def get(self, request, event_id, signup_id):
        signup = self.dal.get_signup(event_id, signup_id)
        serializer = SignUpSerializer(signup)
        return Response(serializer.data)

    def delete(self, request, event_id, signup_id):
        signup = self.dal.get_signup(event_id, signup_id)
        signup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetails(APIView):
    """
    get:
    Get User Email
    """
    dal = DAL()

    def get(self, request):
        signups = self.dal.get_signups_by_email(request.user.email)
        user_request = UserRequest(username=request.user.username, email=request.user.email, signups=signups)
        serializer = UserRequestSerializer(user_request)
        return Response(serializer.data)


class UserSignUpDetails(APIView):
    """
    get:
    Get User's Event SignUp
    put:
    Create User's Event SignUp
    delete:
    Destroy User's Event SignUp
    """
    dal = DAL()
    email_handler = EmailHandler()

    def get(self, request, event_id):
        event = self.dal.get_event(event_id, request.user.email)

        serializer = EventWithoutSignupsSerializer(event)
        return Response(serializer.data)

    def put(self, request, event_id):
        event = self.dal.get_event(event_id)

        signup = self.dal.set_signup(event, request.user.email)
        signup_serializer = SignUpSerializer(signup)

        event_confirmation = EventConfirmationEmail(from_email=request.user.email, to_email=request.user.email,
                                                    event=signup.event)
        self.email_handler.send_email(event_confirmation.get_message())

        return Response(signup_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id):
        self.dal.delete_signup_by_email(event_id, request.user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)
