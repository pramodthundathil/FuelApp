from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput,PasswordInput, Select
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import FuelStocks


class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password1","password2"]
        
        widgets = {
            'username': TextInput(attrs={'class': 'form-control p','placeholder':'User Name'}),
            'first_name': TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),
            'email': TextInput(attrs={'class': 'form-control','placeholder':'Email Id'}),
            "password1": PasswordInput(attrs={'class': 'form-control','placeholder':'Email Id'})

        }


class FuelAddForm(ModelForm):
    class Meta:
        model = FuelStocks
        fields = ["fuel_category","stock"]
        
        widgets = {
            'fuel_category': Select(attrs={'class': 'form-control','placeholder':'Category'}),
            'stock': TextInput(attrs={'class': 'form-control','placeholder':'Stock'}),
            

        }

