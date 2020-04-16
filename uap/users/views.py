from django import forms
from django.http import FileResponse, Http404
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UapUser
from .forms import UserRegisterForm, UapUserUpdateForm, UserUpdateForm



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
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UapUserUpdateForm(request.POST, request.FILES, instance=request.user.uapuser)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', request.user.id)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UapUserUpdateForm(instance=request.user.uapuser)

    ctx = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/update_profile.html', context=ctx)


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = UapUser.objects.get(user=user)
    print(profile.resume.url)
    ctx = {
        'usr': user,
        'profile': profile,
        'bio_length': len(profile.bio),
        'phone_length': len(profile.phone),
        'has_resume': bool(profile.resume.name),
        'website_length': len(profile.website)
    }
    return render(request, 'users/profile.html', context=ctx)


@login_required
def serve_resume(request):
    profile = UapUser.objects.get(user=request.user)
    try:
        return FileResponse(open(profile.resume.url, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')
