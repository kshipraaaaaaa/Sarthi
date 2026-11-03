
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.http import JsonResponse, HttpResponse

from assistance.models import AssistanceRequest
from .models import FamilyInvitation, FamilyConnection, LocationSharing


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


@login_required
def location_sharing(request):

    if request.user.role != 'student':
        return redirect('dashboard')

    sharing, created = LocationSharing.objects.get_or_create(
        student=request.user
    )

    return render(request, 'student/location_sharing.html', {
        'sharing': sharing
    })


@login_required
def update_location(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=405)

    if request.user.role != 'student':
        return JsonResponse({
            'success': False,
            'message': 'Not authorized.'
        }, status=403)

    sharing, created = LocationSharing.objects.get_or_create(
        student=request.user
    )

    enabled = request.POST.get('is_enabled') == 'true'

    if enabled:
        try:
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))

            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise ValueError

        except (TypeError, ValueError):
            return JsonResponse({
                'success': False,
                'message': 'Valid location coordinates are required.'
            }, status=400)

        sharing.latitude = latitude
        sharing.longitude = longitude
        sharing.is_enabled = True

    else:
        sharing.is_enabled = False
        sharing.latitude = None
        sharing.longitude = None

    sharing.save()

    return JsonResponse({
        'success': True,
        'is_enabled': sharing.is_enabled,
        'message': 'Location sharing updated successfully.'
    })



@login_required
def parent_location(request):

    if request.user.role != 'parent':
        return redirect('dashboard')

    try:
        connections = FamilyConnection.objects.filter(
            parent=request.user,
            status='Approved'
        ).select_related('student')

        for connection in connections:
            sharing, created = LocationSharing.objects.get_or_create(
                student=connection.student
            )
            connection.sharing = sharing

        return render(request, 'parent/parent_location.html', {
            'connections': connections
        })

    except Exception as e:
        return HttpResponse(
            f"Error: {type(e).__name__}: {e}",
            status=500
        )
