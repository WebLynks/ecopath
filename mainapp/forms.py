from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number (Optional)'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}),
        }
