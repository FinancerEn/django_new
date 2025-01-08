''' Задаёт логику формы, проверку данных и ограничения.
    Например, проверяет, что сообщение не пустое.

Код в forms.py задаёт правила, которые Django применяет к данным формы.
Шаблон send_message.html отображает форму пользователю.
Все данные, отправленные из HTML-формы, проходят через логику в forms.py на сервере.
'''
from django import forms


class SendMessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Введите сообщение...",
            "rows": 4,
            "class": "form-control"
        }),
        max_length=1000,
        label="Сообщение"
    )

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise forms.ValidationError("Сообщение не может быть пустым.")
        return content
