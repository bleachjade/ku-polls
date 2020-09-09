from django.contrib import admin
from django.urls import path, include

# import polls.views as views

urlpatterns = [
    # path('', views.index),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
