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

from post.models import URP

from .tokens import account_activation_token
from .models import UapUser, FacultyEmail
from .forms import UserRegisterForm, UapStudentUpdateForm, UapFacultyUpdateForm, UserUpdateForm


def register(request):
    """View function for user registration
    """

    # if form is submitted i.e., the http method is POST
    if request.method == 'POST':

        # create instance of form, and populate it with form data in the request object
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            # if form data is valid, create a Userm and set it as inactive, then save
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # get username from the formdata, assign the user into a group:
            # students or faculties
            username = form.cleaned_data.get('username')
            usr = User.objects.get(username=username)
            role = form.cleaned_data['role']
            role = dict(form.fields['role'].choices)[role]

            if role.lower() == 'student':

                # if user chose student, and the email address entered is not a rpi email address,
                # delete the User instance, then redirect to register page and show an error message
                # if email is valid, save the User instance, assign to students group
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

                # if user chose faculty, look up email address in the whitelist (FacultyEmail)
                # if email not in whitelist, delete User instance, redirect to register page and
                # show an error message. Otherwise assign User to faculties group and save instance.
                if FacultyEmail.objects.filter(email=form.cleaned_data['email']).exists():
                    usr.uapuser.is_student = False
                    usr.save()
                    g = Group.objects.get(name='faculties')
                    g.user_set.add(usr)
                else:
                    messages.warning(request, 'The email address you entered is not recognized as a Faculty member.\nPlease contact the admin for further information')
                    User.objects.filter(username=username).delete()
                    return redirect('register')

            # At this point, email address entered by user should either end with @rpi.edu (student)
            # or in the whitelist (faculty). Now send account activation emails for identity verification
            current_site = get_current_site(request)
            subject = 'Activate your UAP account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            # show an instruction message, and redirect to login page
            messages.success(request, 'An confirmation email has been sent to your inbox.\nPlease follow the instructions to activate your account')
            return redirect('login')
    else:

        # Http method is not POST --> create empty form instance for rendering
        form = UserRegisterForm()
    
    # render the page with an empty form
    return render(request, 'users/register.html', {'form': form})


class ActivateAccount(View):
    """Class based view for account activation page
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        """Handles account activation request.
        On success, User instance will be flagged as active

        Parameters:
            request: Django request object
            uidb64: user's id encoded in base 64
            token: one-time-use token for identity vertification
        """

        try:

            # decode user id from uid and get User instance
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):

            # Error indicates the request parameters are not valid
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):

            # if parameters are valid, set User to active and confirm email address
            # redirect to home page and show a success message
            user.is_active = True
            user.uapuser.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been activated')

            return redirect('uap-home')
        else:

            # if not valid, redirect to home page and show an error message
            messages.warning(request, 'The confirmation link is invalid, possibly because it has been already used.')
            return redirect('uap-home')



@login_required
def update_profile(request):
    """Renders the profile update page. Login required
    """

    if request.method == 'POST':

        # POST request:
        # create the user update form (u_form) and profile update form (p_form), and
        # populate them with form data
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if request.user.uapuser.is_student:
            p_form = UapStudentUpdateForm(request.POST, request.FILES, instance=request.user.uapuser)
        else:
            p_form = UapFacultyUpdateForm(request.POST, request.FILES, instance=request.user.uapuser)


        if u_form.is_valid() and p_form.is_valid():

            # save both forms, redirect to profile page, and show a success messgae
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', request.user.id)
    else:

        # GET request:
        # create empty user update form and UAP user update form
        u_form = UserUpdateForm(instance=request.user)
        if request.user.uapuser.is_student:
            p_form = UapStudentUpdateForm(instance=request.user.uapuser)
        else:
            p_form = UapFacultyUpdateForm(instance=request.user.uapuser)

    ctx = {
        'u_form': u_form,
        'p_form': p_form,
    }

    # render profile update page with two empty forms
    return render(request, 'users/update_profile.html', context=ctx)


@login_required
def profile(request, pk):
    """Renders the user profile page. Login required.

    Parameters:
        pk: user id (primary key of User instance)
    """

    user = get_object_or_404(User, pk=pk)
    profile = UapUser.objects.get(user=user)
    ctx = {
        'usr': user,
        'profile': profile,
        'bio_length': len(profile.bio),
        'phone_length': len(profile.phone),
        'has_resume': bool(profile.resume),
        'website_length': len(profile.website),
        'urps': URP.objects.filter(posted_by=user).order_by('-date_posted'),
        'num_urps': URP.objects.filter(posted_by=user).count()
    }
    return render(request, 'users/profile.html', context=ctx)


@login_required
def serve_resume(request):
    """Returns the resume of the user. Login required
    """
    
    profile = UapUser.objects.get(user=request.user)
    try:
        return FileResponse(open(profile.resume.url, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')
