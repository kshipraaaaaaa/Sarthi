from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AssistanceRequestForm
from .models import AssistanceRequest


@login_required
def create_request(request):

    if request.user.role != 'student':
        return redirect('dashboard')

    if request.method == 'POST':

        form = AssistanceRequestForm(request.POST)

        if form.is_valid():

            assistance = form.save(commit=False)
            assistance.student = request.user
            assistance.save()

            return redirect('my_activities')

    else:
        form = AssistanceRequestForm(
            initial={'service': request.GET.get('service', '')}
        )

    return render(
        request,
        'services/create_request.html',
        {'form': form}
    )


@login_required
def my_activities(request):

    if request.user.role != 'student':
        return redirect('dashboard')

    activities = AssistanceRequest.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(
        request,
        'services/my_activities.html',
        {'activities': activities}
    )
