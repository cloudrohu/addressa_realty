from django import forms
from .models import ContactEnquiry

class ContactEnquiryForm(forms.ModelForm):
    class Meta:
        model = ContactEnquiry
        fields = ["type", "name", "email", "phone", "message"]
