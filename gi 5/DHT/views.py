from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import DHT11, Ticket, AuditLog
from .serializers import (
    DHT11Serializer,
    TicketSerializer,
    UserSerializer,
    AuditLogSerializer
)

import smtplib, ssl
from email.message import EmailMessage


# ======================
# CONSTANTS
# ======================
TEMP_MIN, TEMP_MAX = 2, 8
HUM_MIN, HUM_MAX = 40, 70


# ======================
# EMAIL ALERT
# ======================
def send_alert_email(subject, message, recipient):
    email = EmailMessage()
    email.set_content(message)
    email['Subject'] = subject
    email['From'] = settings.DEFAULT_FROM_EMAIL
    email['To'] = recipient

    context = ssl._create_unverified_context()
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(email)
    except Exception as e:
        print("Email error:", e)


# ======================
# AUTH
# ======================
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token)}


@api_view(['POST'])
def register_view(request):
    user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password']
    )
    return Response({
        "token": get_tokens_for_user(user)['access'],
        "user": UserSerializer(user).data
    })


@api_view(['POST'])
def login_view(request):
    user = User.objects.get(email=request.data['email'])
    user = authenticate(username=user.username, password=request.data['password'])
    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)
    return Response({
        "token": get_tokens_for_user(user)['access'],
        "user": UserSerializer(user).data
    })


# ======================
# DHT DATA
# ======================
@api_view(['POST'])
def DhtCreateView(request):
    serializer = DHT11Serializer(data=request.data)
    if serializer.is_valid():
        data = serializer.save()

        alert = (
            data.temperature < TEMP_MIN or data.temperature > TEMP_MAX or
            data.humidity < HUM_MIN or data.humidity > HUM_MAX
        )

        if alert:
            ticket = Ticket.objects.create(
                title="Cold Chain Alert",
                description=f"Sensor {data.sensor_id}",
                status="open"
            )

            AuditLog.objects.create(
                ticket=ticket,
                action="Alert created automatically"
            )

            send_alert_email(
                "Cold Chain Alert",
                f"Temp: {data.temperature} | Hum: {data.humidity}",
                settings.ALERT_EMAIL
            )

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
def Dlist(request):
    data = DHT11.objects.all()
    return Response(DHT11Serializer(data, many=True).data)


# ======================
# TICKETS
# ======================
@api_view(['GET'])
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    return Response(TicketSerializer(tickets, many=True).data)


@api_view(['POST'])
def ticket_create(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        ticket = serializer.save()
        AuditLog.objects.create(ticket=ticket, action="Ticket created")
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PATCH'])
def ticket_update(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.status = request.data.get('status', ticket.status)
    ticket.save()
    AuditLog.objects.create(ticket=ticket, action=f"Status -> {ticket.status}")
    return Response(TicketSerializer(ticket).data)


# ======================
# ALERTS & AUDIT
# ======================
@api_view(['GET'])
def alerts_list(request):
    tickets = Ticket.objects.exclude(status="closed")
    return Response(TicketSerializer(tickets, many=True).data)


@api_view(['GET'])
def audit_list(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return Response(AuditLogSerializer(logs, many=True).data)
