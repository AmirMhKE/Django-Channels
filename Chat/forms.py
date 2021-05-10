from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

user = get_user_model()

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = user
        fields = ('username', 'password1', 'password2',)