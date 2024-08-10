from django import forms
from django.forms import inlineformset_factory
from .models import Client, SalesPipeline, Product, RoomChoices, Order, Campaign

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-center'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-center'}),
        }

class SalesPipelineForm(forms.ModelForm):
    class Meta:
        model = SalesPipeline
        fields = ['current_stage']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'link', 'normal_price', 'discount_price', 'room']
        widgets = {
            'normal_price': forms.TextInput(attrs={'class': 'form-control product-normal-price'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control product-discount-price'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'})
        }


ProductFormSet = inlineformset_factory(Campaign, Product, form=ProductForm, extra=1, can_delete=True)