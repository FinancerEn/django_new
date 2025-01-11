from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Dialog, Message
from .forms import SendMessageForm
from django.contrib.auth.decorators import login_required


# Вывод всех диалогов текущего пользователя:
# Применяем декоратор для обработки случая когда пользователь не аутентифицирован.
# декоратор направит неаутентифицированных пользователей на страницу входа.
@login_required
def dialogs_list(request):
    dialogs = Dialog.objects.filter(participants=request.user).prefetch_related('participants')

    dialogs_with_users = []
    for dialog in dialogs:
        # Находим другого участника диалога
        other_participant = dialog.participants.exclude(id=request.user.id).first()
        dialogs_with_users.append({
            'dialog': dialog,
            'other_participant': other_participant.username if other_participant else "Нет участника",
        })

    context = {"dialogs": dialogs_with_users}
    return render(request, 'messages_app/dialogs_list.html', context)


# Отображение сообщений конкретного диалога:
def dialog_detail(request, dialog_id):
    dialog = get_object_or_404(Dialog.objects.prefetch_related('participants'), id=dialog_id, participants=request.user)
    messages_list = dialog.message_set.all().order_by('timestamp')
    context = {"dialog": dialog, "messages": messages_list}
    return render(request, 'messages_app/dialog_detail.html', context)


# Контроллер для отправки сообщения:
def send_message(request, dialog_id):
    dialog = get_object_or_404(Dialog.objects.prefetch_related('participants'), id=dialog_id)

    if not dialog.participants.filter(id=request.user.id).exists():
        messages.error(request, "Вы не являетесь участником этого диалога.")
        return HttpResponseRedirect(reverse('messages_app:dialogs_list'))

    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            receiver = dialog.participants.exclude(id=request.user.id).first()

            if not receiver:
                messages.error(request, "Ошибка: получатель не найден.")
                return HttpResponseRedirect(reverse('messages_app:dialog_detail', args=[dialog_id]))

            message = Message.objects.create(
                sender=request.user, receiver=receiver, content=content
            )
            dialog.last_message = message
            dialog.save()

            messages.success(request, "Сообщение успешно отправлено.")
            return HttpResponseRedirect(reverse('messages_app:dialog_detail', args=[dialog_id]))
    else:
        form = SendMessageForm()

    context = {"dialog": dialog, "form": form}
    return render(request, 'messages_app/send_message.html', context)
