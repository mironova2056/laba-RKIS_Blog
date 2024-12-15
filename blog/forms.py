from django import forms
from .models import UserProfile, Post, Comment
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'avatar', 'bio']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data
