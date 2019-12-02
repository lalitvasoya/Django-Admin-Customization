from django.utils import timezone
from .models import Profile
from django import forms

class AddDetailForm(forms.ModelForm):
    department = forms.CharField(max_length=10)
    class Meta:
        model = Profile
        fields = ['enrollment','name','semester']
