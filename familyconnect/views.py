from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from assistance.models import AssistanceRequest
from .models import FamilyInvitation, FamilyConnection


def generate_code():
    return get_random_string(8).upper()


@login_required
def family_home(request):

    if request.user.role == 'student':

        invitation, created = FamilyInvitation.objects.get_or_create(
            student=request.user,
            defaults={'code': generate_code()}
        )

        connections = FamilyConnection.objects.filter(
            student=request.user
        ).select_related('parent')

        return render(request, 'familyconnect/student_family.html', {
            'invitation': invitation,
            'connections': connections
        })

    elif request.user.role == 'parent':

       connections = FamilyConnection.objects.filter(
        parent=request.user
    ).select_related('student')

    approved_connections = connections.filter(
        status='Approved'
    )

    student_ids = approved_connections.values_list(
        'student_id', flat=True
    )

    activities = AssistanceRequest.objects.filter(
        student_id__in=student_ids
    ).order_by('-created_at')

    return render(request, 'familyconnect/parent_family.html', {
        'connections': connections,
        'activities': activities
    })
    return redirect('dashboard')


@login_required
def connect_parent(request):

    if request.user.role != 'parent':
        return redirect('dashboard')

    if request.method == 'POST':

        code = request.POST.get('code', '').strip().upper()

        try:
            invitation = FamilyInvitation.objects.get(
                code=code,
                is_active=True
            )

            student = invitation.student

            if student == request.user:
                messages.error(request, "You cannot connect to yourself.")

            else:
                connection, created = FamilyConnection.objects.get_or_create(
                    student=student,
                    parent=request.user
                )

                if created:
                    messages.success(
                        request,
                        "Connection request sent! Waiting for student approval."
                    )

                elif connection.status == 'Rejected':
                    connection.status = 'Pending'
                    connection.save()
                    messages.success(
                        request,
                        "Your connection request has been sent again."
                    )

                else:
                    messages.info(
                        request,
                        "You already have a connection request with this student."
                    )

        except FamilyInvitation.DoesNotExist:
            messages.error(request, "Invalid invitation code.")

    return redirect('family_home')


@login_required
def respond_connection(request, connection_id):

    if request.user.role != 'student':
        return redirect('dashboard')

    connection = get_object_or_404(
        FamilyConnection,
        id=connection_id,
        student=request.user,
        status='Pending'
    )

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'approve':
            connection.status = 'Approved'
            messages.success(request, "Parent connection approved.")

        elif action == 'reject':
            connection.status = 'Rejected'
            messages.info(request, "Parent connection rejected.")

        connection.save()

    return redirect('family_home')