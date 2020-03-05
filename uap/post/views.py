from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import modelform_factory
from ckeditor.widgets import CKEditorWidget
from .forms import URPCreateForm
from .models import URP


def home(request):
    ctx = {
        'urps': URP.objects.all(),
    }
    return render(request, 'post/home.html', ctx)


def about(request):
    return render(request, 'post/about.html')


class URPDetailView(DetailView):
    model = URP


class URPCreateView(CreateView):
    model = URP
    template_name = 'post/urp_create.html'
    form_class = URPCreateForm

    def form_valid(self, form):
        form.instance.posted_by = self.request.user 
        return super().form_valid(form)
    # fields = ['title', 'content']

    

