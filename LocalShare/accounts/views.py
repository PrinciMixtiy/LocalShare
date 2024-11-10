from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

User = get_user_model()


def sign_up_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not (User.objects.filter(username=username).exists() or \
            User.objects.filter(email=email).exists()):
            user = User.objects.create_user(username, email, password)
            login(request, user)

            return redirect(reverse('share:server-file-list'))

        else:
            messages.error(request, "User already exists. Please try again.")

    return render(request, 'authentication/sign-up.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('share:server-file-list'))

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('share:server-file-list'))

        else:
            messages.error(request, "Bad credentials. Please try again.")

    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('share:server-file-list'))

@login_required
def change_password_view(request):
    pass
