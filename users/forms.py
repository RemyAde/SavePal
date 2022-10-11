from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label=_("Password"), 
        strip=False, 
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),)


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email',]
        help_texts = {
            "username":"Your username must be unique. We'll let you know if someone has taken it already.",
            "password1":None,
        }
            


class CustomUserChangeForm(UserChangeForm):


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email',]


