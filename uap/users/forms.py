from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from .models import UapUser, validate_email


class UserRegisterForm(UserCreationForm):
    """Class based form for user registration

    Attributes:
        email (forms.EmailField): requires the users to enter their email addresses.
        role: (forms.ChoiceField): requires the student to choose a role from the given set of roles (Student, Faculty) 
    """
    first_name = forms.CharField(max_length=35, required=True)
    last_name = forms.CharField(max_length=35, required=True)
    email = forms.EmailField(max_length=254, required=True)

    # role of user, either Studeng or Faculty
    role = forms.ChoiceField( choices=[ ('S','Student'), ('F', 'Faculty') ], required=True )

    class Meta:
        """Describes the model to be linked for this form and the order of the fields.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user's firstname and lastname
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UapUserUpdateForm(forms.ModelForm):
    """Form for updating user's phone number, bio (self description), personal website link

    Attributes:
        phone: char field (max_length: 20, not required)
        bio: char field (not required)
        website: URL field (not required)
    """
    phone = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(required=False)
    website = forms.URLField(required=False)
    class Meta:
        model = UapUser
        fields = ['phone', 'bio', 'image', 'resume', 'website']