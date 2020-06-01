from rest_framework import serializers
from ema.models import Event, SignUp, UserRequest
from django.contrib.auth.models import User


# Model Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class EventWithoutSignupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'begin_date', 'end_date', 'location']


class EventSerializer(serializers.ModelSerializer):
    signups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='email')

    def validate(self, attrs):
        """
              Check that start is before finish.
        """
        if attrs['begin_date'] > attrs['end_date']:
            raise serializers.ValidationError("end_date must occur after begin_date")
        return attrs

    class Meta:
        model = Event
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()

    class Meta:
        model = SignUp
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


# Object Serializers

class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    username = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    signups = SignUpSerializer(many=True, allow_null=True, required=False)

    def create(self, validated_data):
        return UserRequest(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        return instance
