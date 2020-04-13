from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ckeditor.fields import RichTextField


class URP(models.Model):

    # title of URP
    title = models.CharField(max_length=100)

    # detailed rich-text description of URP, using ckeditor
    description = RichTextField()

    # summary of URP, used on home page
    summary = models.CharField(max_length=200)

    # date posted, default to server time
    date_posted = models.DateTimeField(default=timezone.now)

    # OP of URP. Currently if the author is deleted, all URPs created by the author will be deleted
    # TODO: revise this design
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # abosolute url for URP detail page
    def get_absolute_url(self):
        return reverse("urp-detail", kwargs={"pk": self.pk})
    


class Application(models.Model):

    # use User as foreign key --> a user can have many applications
    # FIXME: User can only have up to 1 application for a URP, need to check that in views
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)

    # define application status
    APPLYING = 'AP'
    ACCEPTED = 'AC'
    REJECTED = 'RE'
    CANCELED = 'CA'
    STATUS_CHOICES = [
        (APPLYING, 'Applying'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (CANCELED, 'Canceled'),  # application canceled by user, or we can just delete the Application
    ]

    # status of the application
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=APPLYING)

    # the URP the user is applying to
    urp = models.ForeignKey(URP, on_delete=models.CASCADE)

    description = models.CharField(max_length=300, default="")

    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.applicant.username} --{self.status}-> {self.urp.title}'

