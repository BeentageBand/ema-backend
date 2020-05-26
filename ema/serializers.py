from rest_framework import serializers
from ema.models import Event, SignUp, User


# Object Serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        return instance


# Model Serializers

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = SignUp
        fields = '__all__'
