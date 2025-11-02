from django import forms
from .models import ContactSubmission, ServiceCategory

class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = ContactSubmission
        fields = [
            'first_name', 'last_name', 'email', 'mobile_number', 
            'service_inquiry', 'message'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number (Optional)'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_inquiry'].queryset = ServiceCategory.objects.all()
        self.fields['service_inquiry'].empty_label = "Select a service..."
