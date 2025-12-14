from django.db import models
from django.contrib.auth.models import User

# =======================
# Sensor model
# =======================
class DHT11(models.Model):
    sensor_id = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_id} @ {self.dt}"


# =======================
# Ticket model
# =======================
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('assigned', 'Assigné'),
        ('in_progress', 'En cours'),
        ('closed', 'Clos'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


# =======================
# Audit Log model
# =======================
class AuditLog(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="logs"
    )
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.title} - {self.action}"
