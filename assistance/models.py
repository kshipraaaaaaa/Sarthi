

from django.db import models
from django.conf import settings


class AssistanceRequest(models.Model):

    SERVICE_CHOICES = [
        ('Paper Writing', 'Paper Writing Assistance'),
        ('Travel', 'Travel Assistance'),
        ('Digital', 'Digital Assistance'),
        ('Shopping', 'Shopping Assistance'),
        ('Educational', 'Educational Assistance'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Volunteer Assigned'),
        ('Accepted', 'Accepted'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assistance_requests'
    )

    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_requests'
    )

    service = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service} - {self.student.username}"
