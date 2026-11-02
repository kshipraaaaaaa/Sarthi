from django import forms
from .models import AssistanceRequest


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
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Describe the assistance you need...'
                }
            ),
        }