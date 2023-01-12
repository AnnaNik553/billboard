from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserPostListView, logout, register, register_code

app_name = 'users'

urlpatterns = [
    path('posts/', UserPostListView.as_view(), name='user_posts'),
    path('login/', auth_views.LoginView.as_view(template_name='users/user_login.html'), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register_code/<str:username>/', register_code, name='register_code'),
]
