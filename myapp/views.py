from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import Profile,Post, Rating
from .forms import PostForm, RatingsForm, UpdateUserForm, UpdateUserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404,HttpResponseRedirect


# Create your views here.

def welcome(request):
    all_post=Post.objects.all()

    return render(request,'index.html',{"all_post":all_post})

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
    context = {
        'form':form,
    }
    return render(request, 'newpost.html', context)

# @login_required(login_url='/accounts/login/')
# def update_profile(request,username):
#     user =User.objects.get(username=username)
#     if request.method == 'POST':
#         user_from=UpdateUserForm(request.Post,instance=request.user)
#         prof_form=UpdateUserProfileForm(request.Post,request.FILES,instance=request.user.profile)
#         if user_from.is_valid() and prof_form.is_valid():
#             user_from.save
#             prof_form.save
#             return redirect('profile', user.username)
#         else:
#             user_form=UpdateUserForm(instance=request.user) 
#             prof_form=UpdateUserProfileForm(instance=request.user.profile)  
#         params={
#             'user_form':user_form,
#             'prof_form':prof_form,
#         } 
#         return render(request,'update.html',params)     


@login_required(login_url='login')
def update_profile(request):
    # images = request.user.profile.posts.all()
    # images = Post.objects.all()  
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    contex = {
        'user_form': user_form,
        'prof_form': prof_form,
        # 'images': images,

    }
    return render(request, 'update.html', contex)



@login_required(login_url='login')
def project(request,post):
    post=Post.objects.get(title=post)
    ratings=Rating.objects.filter(user=request,post=post).first()
    rating_status=None
    if ratings is None:
        rating_status=False
    else:
        rating_status=True  
    if request.method == 'POST':
        form =RatingsForm(request.POST)
        if form.is_valid():
            rate=form.save(commit=False)
            rate.user=request.user
            rate.post=post
            rate.save()
            post_ratings=Rating.objects.filter(post=post)

            desing_ratings=[d.desing for d in post_ratings]
            desing_avarage=sum(desing_ratings)/len(desing_ratings)

            usability_rating=[usa.usability for usa in post_ratings]
            usability_avarage=sum(usability_rating)/ len(usability_rating)

            content_rating=[cont.content for cont in post_ratings]
            content_avarage=sum(content_rating)/len(content_rating)

            score=(desing_avarage+usability_avarage+content_avarage)/3

            rate.desing_avarage=round(desing_avarage,2)
            rate.usability_avarage=round(usability_avarage,2)
            rate.content_avarage=round(content_avarage,2)
            rate.score=round(score,2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form=RatingsForm()
    params={
        'post':post,
        'rating_form':form,
        'rating_status':rating_status
    }
    return render(request,'singleproject,html', params)  


