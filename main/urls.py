from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.name_user, name='name_user'),
    path('products/<int:product_id>/', views.user_detail, name='user_detail'),
]
