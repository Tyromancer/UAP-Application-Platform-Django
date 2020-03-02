from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import URP


def home(request):
    ctx = {
        'urps': URP.objects.all(),
    }
    return render(request, 'post/home.html', ctx)


def about(request):
    return render(request, 'post/about.html')
