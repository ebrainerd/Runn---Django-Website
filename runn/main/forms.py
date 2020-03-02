from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Max 30 characters.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Max 30 characters.')
    bio = forms.CharField(max_length=250, required=True, help_text='Required. Max 250 characters.')
    location = forms.CharField(max_length=100, required=True, help_text='Required. Max 100 characters.')

    class Meta:
        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'location', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Max 30 characters.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Max 30 characters.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
