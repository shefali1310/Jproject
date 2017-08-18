from django import forms
from models import User,Post, LikeModel, CommentModel


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['email','username','name','password']

class LoginForm(forms.ModelForm) :
    class Meta :
        model = User
        fields = ['username', 'password']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['image', 'caption']

class LikeForm(forms.ModelForm):

    class Meta:
        model = LikeModel
        fields=['post']

class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']

from django import forms

class SearchForm(forms.Form):
    search_query = forms.CharField();