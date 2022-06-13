
from django.contrib import admin
from django.urls import include
from django.urls import re_path



urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'',include ('myapp.urls')),


]
