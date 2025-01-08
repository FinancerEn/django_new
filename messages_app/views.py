from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Dialog, Message
from .forms import SendMessageForm


# Вывод всех диалогов текущего пользователя:
def dialogs_list(request):
    dialogs = Dialog.objects.filter(participants=request.user)
    context = {"dialogs": dialogs}
    return render(request, 'messages_app/dialogs_list.html', context)


# Отображение сообщений конкретного диалога:
def dialog_detail(request, dialog_id):
    dialog = get_object_or_404(Dialog, id=dialog_id, participants=request.user)
    messages_list = dialog.message_set.all().order_by('timestamp')
    context = {"dialog": dialog, "messages": messages_list}
    return render(request, 'messages_app/dialog_detail.html', context)


# Контроллер для отправки сообщения:
def send_message(request, dialog_id):
    dialog = get_object_or_404(Dialog, id=dialog_id)

    # Проверка прав доступа
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

            # Создание сообщения
            message = Message.objects.create(
                sender=request.user, receiver=receiver, content=content
            )
            # Обновление информации о последнем сообщении в диалоге
            dialog.last_message = message
            dialog.save()

            # Уведомление об успешной отправке
            messages.success(request, "Сообщение успешно отправлено.")
            return HttpResponseRedirect(reverse('messages_app:dialog_detail', args=[dialog_id]))
    else:
        form = SendMessageForm()

    context = {"dialog": dialog, "form": form}
    return render(request, 'messages_app/send_message.html', context)
