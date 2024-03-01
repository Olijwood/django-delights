from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account, AccountImage

#Form to Register

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. Add a valid email address")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

#Form to authenticate accounts

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("invalid Login")
        
#Form to update accounts
        
class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username')

#Form to uplaod account images

class AccountImageForm(forms.ModelForm):
    class Meta:
        model = AccountImage
        fields = ['image']
        labels = {
            "image": "Update profile picture:"
        }
