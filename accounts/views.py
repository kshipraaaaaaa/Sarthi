from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm

import logging

logger = logging.getLogger(__name__)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def user_login(request):
    from django.contrib.auth import authenticate

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
    user = authenticate(
        request,
        username=username,
        password=password
    )
        except Exception:
            logger.exception("SAARTHI LOGIN AUTHENTICATION FAILED")
            raise
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):

    if request.user.role == 'student':
        return render(request, 'student/dashboard.html')

    elif request.user.role == 'parent':
        return render(request, 'parent/dashboard.html')

    elif request.user.role in ['nss_volunteer', 'community_volunteer']:
        return render(request, 'volunteer/dashboard.html')

    return redirect('login')
def user_logout(request):
    logout(request)
    return redirect('login')
