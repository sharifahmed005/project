from django.urls import path
from django.urls.conf import include

from .views import *
from .views import RegistrationPage
urlpatterns = [


    path('reg/', RegistrationPage, name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile', profile, name='profile'),


]
