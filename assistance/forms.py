
from django import forms
from .models import AssistanceRequest, EmergencyContact


class AssistanceRequestForm(forms.ModelForm):

    class Meta:
        model = AssistanceRequest

        fields = [
            'service',
            'date',
            'time',
            'venue',
            'description'
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the assistance you need...'
            }),
        }


class EmergencyContactForm(forms.ModelForm):

    class Meta:
        model = EmergencyContact

        fields = [
            'name',
            'relationship',
            'phone',
            'is_primary'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter contact name'
            }),
            'relationship': forms.TextInput(attrs={
                'placeholder': 'e.g. Mother, Father, Guardian'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number',
                'type': 'tel'
            }),
        }

