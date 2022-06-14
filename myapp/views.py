from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Profile,Post, Rating
from .forms import PostForm, RatingsForm, UpdateUserForm, UpdateUserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404,HttpResponseRedirect
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import PostSerializar,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets



# Create your views here.

def welcome(request):
    all_post=Post.objects.all()
    all_post=all_post[::-1]
    a_post = random.randint(0, len(all_post)-1)
    random_post = all_post[a_post]

    return render(request,'index.html',{"all_post":all_post,"random_post":random_post})

def index(request):
    indexpost=Post.objects.filter(id=1)

    return render(request,'index.html',{"all_post":indexpost})    

def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfuly loged in")
            return redirect ("/")
    return render(request,'login.html')

def register(request):
    if request.method == "POST":
        username=request.POST["username"]
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1 !=password2:
            messages.error(request,'Password do not match')
            return render('/register')
        new_user=User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
        ) 
        new_user.save() 
        return render (request,'login.html')
    return render(request,'register.html')

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', params)

def profile(request):
    user=request.user
    my_profile=Profile.objects.get(user=user)
    return render(request,"profile.html",{'my_profile':my_profile,"user":user})

def signout(request):
    logout(request)
    messages.success(request,"You have logged out, we will be glad to have you back again")
    return redirect ("login")

@login_required(login_url='/accounts/login/')
def addpost(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('/')

    else:
        form=PostForm()
    try:
        posts=Post.objects.all() 
        posts=posts[::-1] 
    except Post.DoesNotExist:
        posts=None
    return render(request,'newpost.html',{"form":form,"posts":posts}) 

@login_required(login_url='/accounts/login/')
def postproject(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user=request.user
            project.save()
            
        return redirect('/')
    else:
        form = PostForm()
    try:
        posts=Post.objects.all() 
        posts=posts[::-1]
        a_post = random.randint(0, len(posts)-1)
        random_post = posts[a_post]
    except Post.DoesNotExist:
        posts=None

    context = {
        'form':form,
        'random_post': random_post
    }
    return render(request, 'newpost.html', context)


    


@login_required(login_url='login')
def update_profile(request):
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            # return HttpResponseRedirect(request.path_info)
            return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    contex = {
        'user_form': user_form,
        'prof_form': prof_form,

    }
    return render(request, 'update.html', contex)



 
def search_project(request):
    if request.method == 'GET':
        title = request.GET.get("title")
        results = Post.objects.filter(title__icontains=title).all()
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})

@login_required(login_url='login')
def project(request,post_id):
    post = Post.objects.get(id=post_id)
    ratings = Rating.objects.filter(user=request.user, id=post_id).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    params = {
        'post': post,
        'form': form,
        'rating_status': rating_status

    }
    return render(request, 'singleproject.html', params)


class PostItems(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_list=Post.objects.all()
        serializers=PostSerializar(all_list,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        serializers=PostSerializar(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileItems(APIView):

    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_list=Profile.objects.all()
        user=request.user
        serializers=ProfileSerializer(all_list,many=True)
        return Response(serializers.data,user)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer