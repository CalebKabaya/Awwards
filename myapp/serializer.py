from rest_framework import serializers
from.models import Profile, Post

class PostSerializar(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields=('id','title','description','link','photo','date')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields=('name','bio','location','profile_picture','contact_email')