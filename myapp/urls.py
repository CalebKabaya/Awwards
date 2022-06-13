from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    re_path('^$',views.welcome,name='welcome'),
    re_path('^$',views.index,name='index'),
    re_path('login/',views.signin,name='login'),
    re_path('register/',views.register,name='register'),
    re_path('signout/',views.signout,name='signout'),
    re_path('profile/',views.profile,name='profile'),
    re_path('addpost/',views.addpost,name='addpost'),
    re_path('new-project/', views.postproject, name='newproject'),
    re_path('update', views.update_profile, name='update'),
    re_path('search/', views.search_project, name='search'),
    re_path(r'^vote/(?P<post_id>\d+)?$', views.project, name='vote'), 
    re_path(r'^api/post/$', views.PostItems.as_view()),
    re_path(r'^api/profile/$', views.ProfileItems.as_view())

   
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


   



