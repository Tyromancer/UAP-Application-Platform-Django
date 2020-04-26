from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import URPCreateForm, URPUpdateForm, ApplicationCreateForm, ApplicationManageForm
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


def urp_detail_view(request, pk):
    """Renders the URP detail page
    """

    urp = get_object_or_404(URP, pk=pk)
    ctx = {
        'urp': urp,
    }

    # if user is logged in as a student, check if user has already applied
    if request.user.is_authenticated:
        if request.user.uapuser.is_student:
            ctx['applied'] = Application.objects.filter(applicant=request.user, urp=urp).exists()
        else:
            ctx['applied'] = True

    return render(request, 'post/urp_detail.html', context=ctx)


@login_required
def urp_update_view(request, pk):

    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permission to view this page')
        return redirect('uap-home')

    urp = get_object_or_404(URP, pk=pk)

    if urp.posted_by != request.user:
        messages.warning(request, 'You do not have the permission to view this page')
        return redirect('uap-home')

    if request.method == 'POST':
        form = URPUpdateForm(request.POST)
        if form.is_valid():

            urp.summary = form.cleaned_data['summary']
            urp.description = form.cleaned_data['description']

            urp.save()

            messages.success(request, 'URP updated')
            return redirect('urp-detail', pk=urp.id)

    form = URPUpdateForm(instance=urp)
    ctx = {
        'form': form,
        'id': pk,
    }
    return render(request, 'post/urp_update.html', context=ctx)



@login_required
def urp_create_view(request):

    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    if request.method == 'POST':
        form = URPCreateForm(request.POST)
        if form.is_valid():

            urp = form.save(commit=False)
            urp.posted_by = request.user
            urp.save()

            messages.success(request, 'URP created')
            return redirect('urp-detail', pk=urp.pk)

        messages.warning(request, 'Error when creating URP')
        return redirect('urp-create')

    form = URPCreateForm()
    return render(request, 'post/urp_create.html', context={'form':form})


@login_required
def application_detail_view(request, pk):

    if not request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view the page')
        return redirect('uap-home')

    application = get_object_or_404(Application, pk=pk)
    return render(request, 'post/application_detail.html', context={'application': application})


@login_required
def application_create(request, pk):
    """Renders application creation page. Login required.

    Attribute:
        pk: URP id (primary key of URP instance)
    """
    if not request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    urp = get_object_or_404(URP, pk=pk)
    user = request.user

    if request.method == "POST":
        form = ApplicationCreateForm(request.POST)
        if form.is_valid():

            # save form data to db
            application = form.save(commit=False)
            application.urp = urp
            application.applicant = user
            application.status = Application.APPLYING

            application.save()

            messages.success(request, 'Application created')
            return redirect(f'urp-detail', pk=urp.pk)
    else:
        form = ApplicationCreateForm()

    return render(request, 'post/application_create.html', {'form':form})


@login_required
def application_status(request):
    """Renders the application status page for students. Login required.
    """

    if not request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    user = request.user

    ctx = {
        'applications': Application.objects.filter(applicant=user).order_by('-date_created'),
    }

    return render(request, 'post/application_status.html', ctx)


@login_required
def view_my_urps(request):
    """Displays a list of URPs created by the user. Login required.
    """

    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    user = request.user
    result = list()
    urps = URP.objects.filter(posted_by=user).order_by('-date_posted')

    # get number of active / accepted / rejected applications
    for urp in urps:
        num_active = len(Application.objects.filter(urp=urp, status=Application.APPLYING))
        num_accepted = len(Application.objects.filter(urp=urp, status=Application.ACCEPTED))
        num_rejected = len(Application.objects.filter(urp=urp, status=Application.REJECTED))
        result.append( ( urp, num_active, num_accepted, num_rejected ) )

    ctx = {
        'urps': result
    }

    return render(request, 'post/my_urps.html', ctx)


@login_required
def view_active_applications(request, pk):
    """Displays list of active applications to a specific URP. Login required.

    Parameters:
        pk: URP id (primary key of URP instance)
    """

    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    urp = get_object_or_404(URP, pk=pk)

    ctx = {
        'applications': Application.objects.filter(urp=urp, status=Application.APPLYING).order_by('date_created')
    }

    return render(request, 'post/view_applications.html', ctx)


@login_required
def view_accepted_applications(request, pk):
    """Displays list of accepted applications of a specific URP. Login required.

    Parameters:
        pk: URP id (primary key of URP instance)
    """
    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    urp = get_object_or_404(URP, pk=pk)

    ctx = {
        'applications': Application.objects.filter(urp=urp, status=Application.ACCEPTED).order_by('date_created')
    }
    return render(request, 'post/view_applications.html', ctx)


@login_required
def view_rejected_applications(request, pk):
    """Displays list of rejected applications of a specific URP. Login required.

    Parameters:
        pk: URP id (primary key of URP instance)
    """

    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')
    urp = get_object_or_404(URP, pk=pk)

    ctx = {
        'applications': Application.objects.filter(urp=urp, status=Application.REJECTED).order_by('date_created')
    }
    return render(request, 'post/view_applications.html', ctx)


@login_required
def view_and_manage_application(request, pk):
    """Displays the detail page for a specific application. Login required.

    Parameters:
        pk: Application id (primary key of Application instance)
    """
    if request.user.uapuser.is_student:
        messages.warning(request, 'You do not have the permissions to view this page')
        return redirect('uap-home')

    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':

        # Http method: POST:
        # create form instance and populate with request form data
        form = ApplicationManageForm(request.POST)

        if form.is_valid():
            if application.status == Application.APPLYING:

                # A --> Accepted
                if form.cleaned_data['action'] == 'A':
                    application.status = Application.ACCEPTED
                    application.save()

                # R --> Rejected
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
