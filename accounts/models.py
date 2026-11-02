from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent / Caregiver'),
        ('nss_volunteer', 'NSS Volunteer'),
        ('community_volunteer', 'Community Volunteer'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    contact_no = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

