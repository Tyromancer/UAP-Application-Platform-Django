from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UapUser


@receiver(post_save, sender=User)
def create_uapuser(sender, instance, created, **kwargs):
    if created:
        UapUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_uapuser(sender, instance, **kwargs):
    instance.uapuser.save()