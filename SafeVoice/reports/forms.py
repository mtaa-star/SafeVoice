from django import forms
from .models import ViolenceReport

class ViolenceReportForm(forms.ModelForm):
    class Meta:
        model = ViolenceReport
        fields = ['name', 'contact', 'violence_type', 'description', 'location', 'evidence_file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number or email'
            }),
            'violence_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the incident in detail'
            }),
            'location': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Where did this occur?'
            }),
            'evidence_file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'name': 'Your Name',
            'contact': 'Contact Information',
            'violence_type': 'Type of Violence',
            'description': 'Description of Incident',
            'location': 'County/Location',
            'evidence_file': 'Evidence File (Optional)'
        }

class FollowUpForm(forms.Form):
    report_id = forms.IntegerField(
        label='Report ID',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your report ID'
        })
    )
    contact = forms.CharField(
        max_length=100,
        label='Contact Information',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number or email used in the original report'
        })
    )
    message = forms.CharField(
        label='Follow-up Message',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tell us more about your case or provide an update'
        })
    )
