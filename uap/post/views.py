from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import modelform_factory
from ckeditor.widgets import CKEditorWidget
from .forms import URPCreateForm
from .models import URP


def home(request):
    """Renders the home page of UAP.

    This view will pull all URP entries in the database and list them.
    """
    ctx = {
        'urps': URP.objects.all(),
    }
    return render(request, 'post/home.html', ctx)


def about(request):
    """Renders the about page.
    """
    return render(request, 'post/about.html')


class URPDetailView(DetailView):
    """Class based view for URP detail pages
    """
    model = URP


class URPCreateView(CreateView):
    """Class based view for URP create pages

    Attributes:
        model: sets the model to URP
        template_name (str): path of template used for this view
        form_class: class to be used for creating forms for this view
    """
    model = URP
    template_name = 'post/urp_create.html'
    form_class = URPCreateForm

    def form_valid(self, form):
        """Check if the form is valid
        """
        form.instance.posted_by = self.request.user 
        return super().form_valid(form)
    # fields = ['title', 'content']

    

