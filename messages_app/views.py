from django.shortcuts import render


def dialogs_list(request):
    dialogs = [
        {"username": "User1", "last_message": "Привет!", "timestamp": "10:30"},
        {"username": "User2", "last_message": "Как дела?", "timestamp": "09:15"},
    ]
    context = {"dialogs": dialogs}
    return render(request, 'messages_app/dialogs.html', context)