from rest_framework import serializers
from .models import DHT11, Ticket , AuditLog
from django.contrib.auth.models import User

class DHT11Serializer(serializers.ModelSerializer):
    class Meta:
        model = DHT11
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

from .models import Ticket, AuditLog

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'