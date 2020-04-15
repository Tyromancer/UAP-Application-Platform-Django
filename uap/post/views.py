from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import modelform_factory
from ckeditor.widgets import CKEditorWidget
from .forms import URPCreateForm, ApplicationCreateForm, ApplicationManageForm
from .models import URP, Application


def home(request):
    """Renders the home page of UAP.

    This view will pull all URP entries in the database and list them.
    """
    ctx = {
        'urps': URP.objects.all().order_by('-date_posted'),
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


class URPCreateView(LoginRequiredMixin, CreateView):
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


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    """Class based view for Application detail pages
    """

    model = Application


def application_create(request, pk):
    urp = get_object_or_404(URP, pk=pk)
    username = None
    if request.user.is_authenticated:

        # TODO: show warning message and redirect if user is not a student
        username = request.user.username
    else:
        # redirect to login page if user is not logged in
        messages.warning(request, 'Please login first')
        return redirect('login')

    user = User.objects.get(username=username)
    
    if request.method == "POST":
        form = ApplicationCreateForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.urp = urp
            application.applicant = user
            application.status = Application.APPLYING

            application.save()

            # TODO: display message
            return redirect(f'urp-detail', pk=urp.pk)
    else:
        form = ApplicationCreateForm()
    
    return render(request, 'post/application_create.html', {'form':form})


@login_required
def application_status(request):
    
    user = request.user

    ctx = {
        'applications': Application.objects.filter(applicant=user).order_by('-date_created'),
    }

    return render(request, 'post/application_status.html', ctx)


@login_required
def view_my_urps(request):

    user = request.user

    result = list()
    urps = URP.objects.filter(posted_by=user).order_by('-date_posted')
    for urp in urps:
        result.append( ( urp, len(Application.objects.filter(urp=urp, status=Application.APPLYING)) ) )
    
    ctx = {
        'urps': result
    }

    return render(request, 'post/my_urps.html', ctx)


@login_required
def view_applications(request, pk):

    urp = get_object_or_404(URP, pk=pk)

    if request.user.is_authenticated:

        # TODO: show warning message and redirect if user is not faculty
        pass
    else:

        # redirect to login page if user is not logged in
        messages.warning(request, 'Please login first')
        return redirect('login')

    ctx = {
        'applications': Application.objects.filter(urp=urp, status=Application.APPLYING).order_by('date_created')
    }

    return render(request, 'post/view_applications.html', ctx)


@login_required
def view_and_manage_application(request, pk):

    # TODO: check if user is faculty
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationManageForm(request.POST)
        if form.is_valid():
            if application.status == Application.APPLYING:
                if form.cleaned_data['action'] == 'A':
                    application.status = Application.ACCEPTED
                    application.save()

                elif form.cleaned_data['action'] == 'R':
                    application.status = Application.REJECTED
                    application.save()

                messages.success(request, 'Success!')
            return redirect(request.get_full_path())

    form = ApplicationManageForm()
    ctx = {
        'application':application,
        'form':form,
    }
    return render(request, 'post/manage_application.html', context=ctx)


    
# class ApplicationCreateView(CreateView):
#     """Class based view for creating applications for URPs
#     """

#     model = Application
#     template_name = 'post/application_create.html'
#     form_class = ApplicationCreateForm

#     def form_valid(self, form):

#         form.instance.posted_by = self.request.user
#         return super().form_valid(form)
