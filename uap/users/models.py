from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from ckeditor.fields import RichTextField
from PIL import Image



# TODO: for both profiles, add relations to URPs

class UapUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True)
    bio = RichTextField(default='')
    resume = models.FileField(default='default.pdf', upload_to='resumes')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    website = models.URLField()
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.lastname}'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# class FacultyProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=100, blank=False)
#     email = models.EmailField(unique=True)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     website = models.URLField()

#     def __str__(self):
#         return f'{self.user.username}'

#     def save(self):
#         super().save()

#         img = Image.open(self.image.path)
#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)


# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_student.lower() == 'student':
#             StudentProfile.objects.create(user=instance)
#         elif instance.is_student.lower() == 'faculty':
#             FacultyProfile.objects.create(user=instance)
#         else:
#             pass
#     instance.profile.save()
