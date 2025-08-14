from django import forms
from .models import Internship, InternshipApplication, HouseProject

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        exclude = ['firm']

class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        exclude = ['internship', 'student']

class HouseProjectForm(forms.ModelForm):
    class Meta:
        model = HouseProject
        exclude = ['client', 'firm', 'status', 'approval_message', 'firm_response', 'approved_by_firm', 'submitted_at']