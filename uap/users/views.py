from django import forms
from django.views.generic import View
from django.http import FileResponse, Http404
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy

from .tokens import account_activation_token
from .models import UapUser, FacultyEmail
from .forms import UserRegisterForm, UapUserUpdateForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            usr = User.objects.get(username=username)
            role = form.cleaned_data['role']
            role = dict(form.fields['role'].choices)[role]

            if role.lower() == 'student':
                if not form.cleaned_data['email'].endswith('@rpi.edu'):
                    messages.warning(request, 'The email address you entered is not a valid RPI email address')
                    User.objects.filter(username=username).delete()
                    return redirect('register')
                else:
                    usr.uapuser.is_student = True
                    usr.save()
                    g = Group.objects.get(name='students')
                    g.user_set.add(usr)
            elif role.lower() == 'faculty':
                # TODO
                if FacultyEmail.objects.filter(email=form.cleaned_data['email']).exists():
                    usr.uapuser.is_student = False
                    usr.save()
                    g = Group.objects.get(name='faculties')
                    g.user_set.add(usr)
                else:
                    messages.warning(request, 'The email address you entered is not recognized as a Faculty member.\nPlease contact the admin for further information')
                    User.objects.filter(username=username).delete()
                    return redirect('register')

            current_site = get_current_site(request)
            subject = 'Activate your UAP account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'An confirmation email has been sent to your inbox.\nPlease follow the instructions to activate your account')
            return redirect('login')

            # username = form.cleaned_data.get('username')

            # user = User.objects.get(username=username)
            # role = form.cleaned_data['role']
            # role = dict(form.fields['role'].choices)[role]
            # if role.lower() == 'student':
            #     g = Group.objects.get(name='students')
            #     g.user_set.add(user)
            # elif role.lower() == 'faculty':
            #     g = Group.objects.get(name='faculties')
            #     g.user_set.add(user)

            # TODO: handle when role is neither of those
            # TODO: check if user is actually faculty member

            # messages.success(request, f'Your account has been created!')
            # return redirect('uap-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.uapuser.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been activated')

            return redirect('uap-home')
        else:
            messages.warning(request, 'The confirmation link is invalid, possibly because it has been already used.')
            return redirect('uap-home')



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
    ctx = {
        'usr': user,
        'profile': profile,
        'bio_length': len(profile.bio),
        'phone_length': len(profile.phone),
        'has_resume': bool(profile.resume),
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
