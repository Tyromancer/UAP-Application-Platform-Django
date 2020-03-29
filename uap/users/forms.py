from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """Class based form for user registration

    Attributes:
        email (forms.EmailField): requires the users to enter their email addresses.
        role: (forms.ChoiceField): requires the student to choose a role from the given set of roles (Student, Faculty) 
    """
    email = forms.EmailField(required=True)

    # role of user, either Studeng or Faculty
    role = forms.ChoiceField( choices=[ ('S','Student'), ('F', 'Faculty') ], required=True )

    class Meta:
        """Describes the model to be linked for this form and the order of the fields.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']
