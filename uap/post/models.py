from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class URP(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    contactant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
