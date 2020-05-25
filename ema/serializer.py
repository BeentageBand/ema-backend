from rest_framework import serializers
from ema.models import Event, SignUp


class EventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    begin_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = Event
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    event = EventSerializer(required=False)
    email = serializers.EmailField(required=False)
    signup_date = serializers.DateTimeField(required=False)

    class Meta:
        model = SignUp
        fields = '__all__'
