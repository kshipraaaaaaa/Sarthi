from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'gender',
        'age',
        'contact_no',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [
    ('student', 'Student'),
    ('parent', 'Parent / Caregiver'),
    ('nss_volunteer', 'NSS Volunteer'),
    ('community_volunteer', 'Community Volunteer'),
]
