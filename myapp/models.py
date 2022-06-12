from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField



# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture=CloudinaryField('image')
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
    photo=CloudinaryField('image')
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

class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'
