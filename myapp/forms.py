from django import forms
from .models import Post, Profile,Rating
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    photo=forms.ImageField(label="")
    class Meta:
        model=Post
        fields=('photo','title','link','description')

class UpdateUserForm(forms.ModelForm):
    email=forms.EmailField(max_length=254,help_text='Required.Inform a valid email addres')
    class Meta:
        model= User
        fields=('username','email')

class UpdateUserProfileForm(forms.ModelForm):
    email=forms.EmailField(max_length=254,help_text='Required.Inform a valid email addres')
    class Meta:
        model= Profile
        fields=('name','bio','profile_picture','location','contact_email')


class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design', 'usability', 'content']