from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# from pyuploadcare.dj.models import ImageField


# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture=models.ImageField(upload_to='images/', default='default.png')
    bio=models.TextField(max_length=500,default="My Bio",blank=True)
    name=models.CharField(max_length=120,blank=True)
    location=models.CharField(max_length=100,blank=True)
    contact_email=models.EmailField(max_length=100,blank=True)

    def __str__(self):
        return f'{self.user.username}Profile'
    @receiver(post_save,sender=User) 
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save,sender=User) 
    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()


class Post(models.Model):
    title=models.CharField(max_length=160)
    link=models.URLField(max_length=300)
    description=models.TextField(max_length=300)
    technologies=models.CharField(max_length=200,blank=True)
    photo=models.ImageField(upload_to='pictures/')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    date=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return f'{self.title}'

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def all_posts(cls):
        return cls.objects.all()


    @classmethod
    def search_projects(cls,title):
        return cls.objects.filter(title__icontains=title).all()    



