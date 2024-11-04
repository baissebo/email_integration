from django.shortcuts import render
from .models import EmailAccount
from .utils import fetch_messages


def message_list(request):
    error_message = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            account = EmailAccount.objects.get(email=email)

            if account.check_password(password):
                messages = fetch_messages(account, password)
                return render(request, "message_list.html", {"messages": messages})

            else:
                error_message = "Неверный пароль."

        except EmailAccount.DoesNotExist:
            error_message = "Аккаунт с таким Email не существует."

    return render(request, "message_list.html", {"messages": [], "error_message": error_message})
