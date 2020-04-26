from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import EmailValidator
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(email):
    if not FacultyEmail.objects.filter(email=email).exists():
        if not email.strip().endswith('@rpi.edu'):
            raise ValidationError(
                _(f'{email} is not a valid rpi email address')
            )


class UapUser(models.Model):
    """ UapUser is a composition class of the Django User model and more fields for extra information.

    Attributes:
        user (models.OneToOneField): links the Django User class
        email (models.EmailField): stores the user's email address, should be unique
        phone (models.CharField): stores the user's phone number. Has a maximum of 20 characters, and can be empty.
        bio (models.CharField): stores the user's bio in rich text.
        resume (models.FileField): stores the path to the user's uploaded resume. The uploaded file will be under the 'resumes' directory
        image (models.ImageField): stores the path to the user's avatar image. The uploaded image will be under the 'profile_pics' directory. TODO: change this when deploying.
        website (models.URLField): stores the URL of the user's personal website.
        is_student (models.BooleanField): indicates the role of user: True -> student, False -> faculty. This defaults to true.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, default='')
    bio = RichTextField(default='')
    resume = models.FileField(blank=True, upload_to='resumes')
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    website = models.URLField()
    is_student = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        """Defines the behavior when an UapUser instance is saved.

        First call save() from parent class, then crop and save image.
        """
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FacultyEmail(models.Model):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.email}'
