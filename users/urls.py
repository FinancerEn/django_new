from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path('friends/', views.friends_list, name='friends_list'),
]
