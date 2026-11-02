from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent / Caregiver'),
        ('nss_volunteer', 'NSS Volunteer'),
        ('community_volunteer', 'Community Volunteer'),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )