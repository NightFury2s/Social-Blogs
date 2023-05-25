from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import (
    UserRegistrationForm,
    LoginForm,
)

# Create your views here.

def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Sai username hoặc password")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Đăng ký thành công")
            return redirect('login')

    context = {
        "form": form
    }
    return render(request, 'registration.html', context)

def profile(request):
    return render(request, 'profile.html')