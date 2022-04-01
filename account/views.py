from .forms import CreateUserForm, UpdateUser
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect!')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def RegistrationPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account Was Created for ' + username)
            return redirect('/accounts/login')

    context = {
        'forms': form
    }
    return render(request, 'registration.html', context)


def profile(request):
    form = UpdateUser()
    if request.method == 'POST':
        form = UpdateUser(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'User Update Successfully.')
            return redirect('/profile')

    context = {
        'forms': form
    }
    return render(request, 'profile.html', context)
