from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import UapUser
from .forms import UserRegisterForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            user = User.objects.get(username=username)
            role = form.cleaned_data['role']
            role = dict(form.fields['role'].choices)[role]
            if role.lower() == 'student':
                g = Group.objects.get(name='students')
                g.user_set.add(user)
            elif role.lower() == 'faculty':
                g = Group.objects.get(name='faculties')
                g.user_set.add(user)

            # TODO: handle when role is neither of those
            # TODO: check if user is actually faculty member

            messages.success(request, f'Your account has been created!')
            return redirect('uap-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
