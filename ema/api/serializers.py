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
