from django import forms
from .models import Post



class PostForm(forms.ModelForm):
    photo=forms.ImageField(label="")
    class Meta:
        model=Post
        fields=('photo','title','link','description')

