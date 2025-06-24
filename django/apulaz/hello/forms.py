from django import forms
from .models import Topic, Post
from django.contrib.auth.models import User

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordResetForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    
    class Meta:
        model = User
        fields = []

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data["new_password"]
        user.set_password(new_password)
        if commit:
            user.save()
        return user
