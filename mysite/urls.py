from os import name
from mysite.views import index
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name="main_index"),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]