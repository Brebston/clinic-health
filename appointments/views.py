from __future__ import annotations

from datetime import datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from doctors.models import DoctorProfile
from .forms import AppointmentCreateForm
from .models import Appointment


@login_required
def appointment_create(request):
    """
    Booking page handler.
    GET: show form
    POST: validate + create appointment
    """

    specialties = DoctorProfile.Specialty.choices

    if request.method == "POST":
        # You can either use the form OR raw POST parsing.
        # Form gives you validation for day/time_str.
        form = AppointmentCreateForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest("Invalid form data")

        doctor = form.cleaned_data["doctor"]
        day = form.cleaned_data["day"]
        notes = (form.cleaned_data.get("notes") or "").strip()

        starts_at = form.build_starts_at()
        if starts_at <= timezone.now():
            return HttpResponseBadRequest("Cannot book in the past")

        # Convert time_str -> time for storing as TimeField
        hh, mm = form.cleaned_data["time_str"].split(":")
        tm = time(int(hh), int(mm))

        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=day,
            appointment_time=tm,
        ).exists():
            return HttpResponseBadRequest("Slot already booked")

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=day,
            appointment_time=tm,
            notes=notes,
            status=Appointment.STATUS_BOOKED,
        )

        return redirect("appointments:my-visits")

    # GET
    form = AppointmentCreateForm()
    return render(
        request,
        "core/appointment.html",
        {"specialties": specialties, "form": form},
    )


@login_required
def my_visits(request):
    """
    Patient: sees own visits (upcoming/past)
    Doctor: sees own visits for patients (upcoming/past/all)
    Filters: scope + status
    """

    doctor_profile = getattr(request.user, "doctor_profile", None)
    is_doctor = bool(doctor_profile)

    qs = Appointment.objects.filter(doctor=doctor_profile) if is_doctor else Appointment.objects.filter(patient=request.user)

    scope = request.GET.get("scope", "upcoming").strip()
    status_filter = request.GET.get("status", "").strip()

    if status_filter:
        qs = qs.filter(status=status_filter)

    now = timezone.localtime()
    today = now.date()
    now_time = now.time()

    past_q = Q(appointment_date__lt=today) | Q(appointment_date=today, appointment_time__lt=now_time)
    upcoming_q = Q(appointment_date__gt=today) | Q(appointment_date=today, appointment_time__gte=now_time)

    if scope == "past":
        qs = qs.filter(past_q)
    elif scope == "all" and is_doctor:
        pass
    else:
        qs = qs.filter(upcoming_q)

    visits = qs.order_by("-appointment_date", "-appointment_time")

    return render(request, "appointments/my_visits.html", {
        "visits": visits,
        "is_doctor": is_doctor,
        "scope": scope,
        "status_filter": status_filter,
        "STATUS_CHOICES": Appointment.STATUS_CHOICES,
    })


@login_required
def cancel_visit(request, pk: int):
    """
    Patient can cancel only own appointment.
    Doctor can cancel only appointments assigned to them.
    """

    appt = get_object_or_404(Appointment, pk=pk)

    doctor_profile = getattr(request.user, "doctor_profile", None)
    is_doctor = bool(doctor_profile)

    if is_doctor:
        if appt.doctor_id != doctor_profile.id:
            return HttpResponseBadRequest("Not allowed")
    else:
        if appt.patient_id != request.user.id:
            return HttpResponseBadRequest("Not allowed")

    # Optional rule: don't allow cancelling completed appointments
    if appt.status == Appointment.STATUS_COMPLETED:
        return HttpResponseBadRequest("Cannot cancel completed appointment")

    appt.status = Appointment.STATUS_CANCELLED
    appt.save(update_fields=["status"])
    return redirect("appointments:my-visits")


@login_required
def update_status(request, pk: int):
    """
    Doctor-only status update.
    """

    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    appt = get_object_or_404(Appointment, pk=pk)

    doctor_profile = getattr(request.user, "doctor_profile", None)
    if not doctor_profile or appt.doctor_id != doctor_profile.id:
        return HttpResponseBadRequest("Not allowed")

    status = (request.POST.get("status") or "").strip()
    allowed = {c[0] for c in Appointment.STATUS_CHOICES}
    if status not in allowed:
        return HttpResponseBadRequest("Invalid status")

    appt.status = status
    appt.save(update_fields=["status"])
    return redirect("appointments:my-visits")


@login_required
def api_doctors_by_specialty(request):
    """
    Returns doctors filtered by specialty for dynamic dropdown in booking page.
    """

    specialty = request.GET.get("specialty")
    if not specialty:
        return JsonResponse({"doctors": []})

    doctors = DoctorProfile.objects.filter(specialty=specialty).select_related("user")

    data = [{"id": d.id, "name": str(d)} for d in doctors]
    return JsonResponse({"doctors": data})


@login_required
def api_available_times(request):
    """
    Returns available time slots for a given doctor + day.
    Used by 'Show Available Times' button without page reload.
    """

    doctor_id = request.GET.get("doctor")
    date_str = request.GET.get("date")

    if not doctor_id or not date_str:
        return JsonResponse({"times": []})

    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    try:
        day = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"times": []})

    # Business hours
    start = time(8, 30)
    end = time(17, 0)
    step_minutes = 30

    busy = set(
        Appointment.objects.filter(
            doctor=doctor,
            appointment_date=day,
        ).values_list("appointment_time", flat=True)
    )

    tz = timezone.get_current_timezone()
    now = timezone.now()

    times = []
    cur = timezone.make_aware(datetime.combine(day, start), tz)
    end_dt = timezone.make_aware(datetime.combine(day, end), tz)

    while cur < end_dt:
        if cur.time() not in busy and cur > now:
            times.append(cur.strftime("%H:%M"))
        cur += timedelta(minutes=step_minutes)

    return JsonResponse({"times": times})
