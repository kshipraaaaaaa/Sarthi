
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import EmergencyContact
from .forms import EmergencyContactForm
from .forms import AssistanceRequestForm
from .models import AssistanceRequest


# Check whether the logged-in user is a volunteer
def is_volunteer(user):
    return user.role in ['nss_volunteer', 'community_volunteer']


# ---------------- STUDENT FUNCTIONS ----------------

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


# ---------------- VOLUNTEER FUNCTIONS ----------------

@login_required
def available_requests(request):

    if not is_volunteer(request.user):
        return redirect('dashboard')

    activities = AssistanceRequest.objects.filter(
        status='Pending',
        volunteer__isnull=True
    ).order_by('date', 'time')

    return render(
        request,
        'assistance/available_requests.html',
        {'activities': activities}
    )


@login_required
def accept_request(request, request_id):

    if not is_volunteer(request.user):
        return redirect('dashboard')

    if request.method == 'POST':

        with transaction.atomic():

            activity = get_object_or_404(
                AssistanceRequest.objects.select_for_update(),
                id=request_id
            )

            if activity.status == 'Pending' and activity.volunteer is None:

                activity.volunteer = request.user
                activity.status = 'Accepted'
                activity.save()

                messages.success(
                    request,
                    "Request accepted successfully!"
                )

            else:
                messages.error(
                    request,
                    "Sorry! This request has already been accepted."
                )

    return redirect('available_requests')


@login_required
def volunteer_activities(request):

    if not is_volunteer(request.user):
        return redirect('dashboard')

    activities = AssistanceRequest.objects.filter(
        volunteer=request.user
    ).order_by('-created_at')

    return render(
        request,
        'assistance/volunteer_activities.html',
        {'activities': activities}
    )
@login_required
def emergency_contacts(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    contacts = EmergencyContact.objects.filter(student=request.user)

    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.student = request.user

            if contact.is_primary:
                EmergencyContact.objects.filter(
                    student=request.user
                ).update(is_primary=False)

            contact.save()
            messages.success(request, 'Emergency contact added successfully!')
            return redirect('emergency_contacts')
    else:
        form = EmergencyContactForm()

    return render(request, 'student/emergency_contacts.html', {
        'contacts': contacts,
        'form': form
    })


@login_required
def edit_emergency_contact(request, contact_id):
    contact = get_object_or_404(
        EmergencyContact, id=contact_id, student=request.user
    )

    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            updated = form.save(commit=False)

            if updated.is_primary:
                EmergencyContact.objects.filter(
                    student=request.user
                ).exclude(id=contact.id).update(is_primary=False)

            updated.save()
            messages.success(request, 'Contact updated!')
            return redirect('emergency_contacts')
    else:
        form = EmergencyContactForm(instance=contact)

    return render(request, 'assistance/edit_emergency_contact.html', {
        'form': form
    })


@login_required
def delete_emergency_contact(request, contact_id):
    contact = get_object_or_404(
        EmergencyContact, id=contact_id, student=request.user
    )

    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted!')

    return redirect('emergency_contacts')
