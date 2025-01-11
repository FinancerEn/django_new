from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def friends_list(request):
    # Пример: список друзей текущего пользователя
    user = request.user
    # Пример: Поищем друзей как другие пользователи, которые добавлены в поле friends
    friends = user.friends.all()  # Допустим, у пользователя есть поле friends, которое связывает его с другими пользователями

    return render(request, 'users/friends_list.html', {"friends": friends})


def user_login(request):
    # Перенаправление, если пользователь уже вошёл
    if request.user.is_authenticated:
        return redirect("main:index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Это встроенная функция Django для проверки имени пользователя и пароля.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main:index")
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    return render(request, "users/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("main:index")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Аутентифицируем и логиним пользователя
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Берём пароль из формы
            user = authenticate(request, username=username, password=password)
            # Если пользователь успешно аутентифицирован, вызываем login() для входа.
            # пользователь сразу же будет считаться вошедшим в систему после регистрации.
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрировались и вошли!')
                return redirect("main:index")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
