from django import forms
from .models import Client, SalesPipeline

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'email', 'address']

class SalesPipelineForm(forms.ModelForm):
    class Meta:
        model = SalesPipeline
        fields = ['current_stage']