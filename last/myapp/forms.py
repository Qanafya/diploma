from django import forms
from .models import *

class ChefForm(forms.ModelForm):
    class Meta:
        model = Chef
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class ChefLog(forms.ModelForm):
    class Meta:
        model = Jur
        fields = ['user_id', 'role']

class JurForm(forms.ModelForm):
    class Meta:
        model = Jur
        fields = '__all__'

class ChefDetailForms(forms.ModelForm):
    class Meta:
        model = ChefDetail
        fields = '__all__'

class CustomerInfoForms(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'