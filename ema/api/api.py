from ema.api.dal import DAL
from ema.api.permissions import IsAdminOrReadOnly
from ema.api.serializers import *
from ema.email.confirmationemail import EventConfirmationEmail
from ema.email.emailhandler import EmailHandler
from ema.models import UserRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView


# APIs

class EventList(ListCreateAPIView):
    """
    get:
    Get all the events of all existing users
    post:
    Create a new event
    """
    dal = DAL()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = EventSerializer

    def get_queryset(self):
        return self.dal.list_events()


class EventDetails(RetrieveUpdateDestroyAPIView):
    """
    get:
    Get Event Details from given Event Id
    put:
    Update Event Details from given Event Id
    delete:
    Delete Event Details from given Event Id. SignUps are removed altogether.
    """
    dal = DAL()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = EventSerializer
    lookup_field = 'event_id'

    def get_object(self):
        event_id = self.kwargs['event_id']
        return self.dal.get_event(event_id)


class EventSignUp(ListCreateAPIView):
    """
    get:
    List all SignUps for a given Event Id
    post:
    Create a new SignUp for a given Event Id
    """
    dal = DAL()
    serializer_class = SignUpSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'event_id'

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return self.dal.get_event(event_id).signups

    def create(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        event = self.dal.get_event(event_id)
        user_serializer = UserRequestSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_request = user_serializer.save()

        signup = self.dal.set_signup(event, user_request.email)
        signup_serializer = SignUpSerializer(signup)

        return Response(signup_serializer.data, status=status.HTTP_201_CREATED)


class SignUpDetails(RetrieveUpdateDestroyAPIView):
    """
    get:
    Get Signup Details for given Event Id and SignUp Id
    put:
    Update Signup Details for given Event Id and SignUp Id
    delete:
    Destroy Signup Details for given Event Id and SignUp Id
    """
    dal = DAL()
    permission_classes = [IsAdminUser]
    serializer_class = SignUpSerializer
    lookup_field = 'event_id'

    def get_object(self):
        event_id = self.kwargs['event_id']
        signup_id = self.kwargs['signup_id']
        return self.dal.get_signup(event_id, signup_id)


class UserCreate(CreateAPIView):
    """
    Create a new User
    """
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserDetails(RetrieveAPIView):
    """
    get:
    Get User Email
    """
    dal = DAL()
    serializer_class = UserRequestSerializer
    lookup_field = 'event_id'

    def get_object(self):
        signups = self.dal.get_signups_by_email(self.request.user.email)
        return UserRequest(username=self.request.user.username, email=self.request.user.email, signups=signups)


class UserSignUpDetails(RetrieveUpdateDestroyAPIView):
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
    serializer_class = SignUpSerializer

    def get_object(self):
        event_id = self.kwargs['event_id']
        event = self.dal.get_event(event_id)
        signup = self.dal.get_signup_by_email_or_raise(event, self.request.user.email)
        return signup[0]

    def update(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        event = self.dal.get_event(event_id)

        signup = self.dal.set_signup(event, request.user.email)
        signup_serializer = SignUpSerializer(signup)

        event_confirmation = EventConfirmationEmail(from_email=request.user.email, to_email=request.user.email,
                                                    event=signup.event)
        self.email_handler.send_email(event_confirmation.get_message())

        return Response(signup_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        event_id = kwargs['event_id']
        self.dal.delete_signup_by_email(event_id, request.user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)
