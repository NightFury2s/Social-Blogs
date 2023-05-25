from django.urls import path
from user_profile.views import login_user
from .views import *

urlpatterns = [
    path('login/', login_user, name='login')
]