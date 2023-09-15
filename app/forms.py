from django import forms
from .models import *

class User_Profile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_address_1','user_address_2', 'user_pincode' , 'user_email' , 'user_phone']
        


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
