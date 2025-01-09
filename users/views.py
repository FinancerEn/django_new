from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


def friends_list(request):
    # Пример: список друзей текущего пользователя
    user = request.user
    # Пример: Поищем друзей как другие пользователи, которые добавлены в поле friends
    friends = user.friends.all()  # Допустим, у пользователя есть поле friends, которое связывает его с другими пользователями

    return render(request, 'users/friends_list.html', {"friends": friends})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main:index")
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, "users/login.html")
