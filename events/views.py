# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .models import Event, Registration
from .utils import extract_registration_schema


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ["start_time"]
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        location = self.request.GET.get("location")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current search params back to the template
        context["current_query"] = self.request.GET.get("q", "")
        context["current_location"] = self.request.GET.get("location", "")
        return context


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/user_events.html"
    context_object_name = "hosted_events"

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch events the user is attending (registered for)
        # We want the Registration objects to show status, or just the events?
        # The prompt says: "Mission Assignments": Events the user is attending. Show their current status.
        # So we should probably fetch the Registration objects for this user.
        context["attended_registrations"] = (
            Registration.objects.filter(participant=self.request.user)
            .select_related("event")
            .order_by("event__start_time")
        )
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            # Get user's specific registration to check status
            user_registration = Registration.objects.filter(
                event=event, participant=user
            ).first()

            context["is_registered"] = user_registration is not None
            context["user_registration"] = user_registration

            # If organizer, get all registrations
            if user == event.organizer:
                context["registrations"] = Registration.objects.filter(
                    event=event
                ).select_related("participant", "participant__profile")
        else:
            context["is_registered"] = False

        return context


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time", "location", "capacity"]
    template_name = "events/event_form.html"
    success_message = "Event '%(title)s' was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass an empty schema for new events if we want to default it
        # context["schema_json"] = "[]"
        return context

    def form_valid(self, form):
        form.instance.organizer = self.request.user

        form.instance.registration_schema = extract_registration_schema(
            self.request.POST
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"slug": self.object.slug})


class EventUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Event
    fields = ["title", "description", "start_time", "end_time", "location", "capacity"]
    template_name = "events/event_form.html"
    success_message = "Event '%(title)s' was updated successfully"

    def form_valid(self, form):
        form.instance.organizer = self.request.user

        form.instance.registration_schema = extract_registration_schema(
            self.request.POST
        )

        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.organizer:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"slug": self.object.slug})


class EventDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("user-events")
    success_message = "Event was deleted successfully"

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.organizer:
            return True
        return False


class EventRegistrationView(LoginRequiredMixin, View):
    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        # Check if already registered
        if Registration.objects.filter(event=event, participant=request.user).exists():
            messages.warning(request, "You are already registered for this mission.")
            return redirect("event-detail", slug=slug)

        # Capture Answers if schema exists
        answers = {}
        if event.registration_schema:
            for question in event.registration_schema:
                key = f"answer_{question['id']}"
                if question.get("type") == "checkbox":
                    answers[question["id"]] = request.POST.get(key) == "on"
                else:
                    answers[question["id"]] = request.POST.get(key, "")

        # Check capacity
        current_registrations = event.registrations.filter(status="registered").count()
        status = "registered"

        if current_registrations >= event.capacity:
            status = "waitlisted"
            msg_type = messages.INFO
            msg_text = "Mission capacity reached. You have been placed on the standby (wait) list."
        else:
            status = "registered"
            msg_type = messages.SUCCESS
            msg_text = f"Successfully registered for mission: {event.title}"

        # Create registration
        Registration.objects.create(
            event=event, participant=request.user, status=status, answers=answers
        )

        # Flash message
        if msg_type == messages.INFO:
            messages.info(request, msg_text)
        else:
            messages.success(request, msg_text)

        return redirect("event-detail", slug=slug)


class EventUnregistrationView(LoginRequiredMixin, View):
    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        registration = Registration.objects.filter(
            event=event, participant=request.user
        ).first()

        if registration:
            registration.delete()
            messages.info(request, f"You have withdrawn from mission: {event.title}")
        else:
            messages.warning(request, "Registration record not found.")

        return redirect("event-detail", slug=slug)


from django.core.mail import send_mail


import csv
from django.http import HttpResponse


class EventExportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{event.slug}_roster.csv"'
        )

        writer = csv.writer(response)

        # Header row
        headers = ["Username", "Email", "Status", "Registered At"]

        # Add dynamic headers from schema
        question_ids = []
        if event.registration_schema:
            for question in event.registration_schema:
                headers.append(question["label"])
                question_ids.append(question["id"])

        writer.writerow(headers)

        # Data rows
        registrations = event.registrations.select_related("participant").all()
        for reg in registrations:
            row = [
                reg.participant.username,
                reg.participant.email,
                reg.status,
                reg.registered_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]

            # Add dynamic answers
            if event.registration_schema:
                for q_id in question_ids:
                    # Retrieve answer safely, handle booleans for checkboxes
                    answer = reg.answers.get(q_id, "")
                    if isinstance(answer, bool):
                        answer = "Yes" if answer else "No"
                    row.append(answer)

            writer.writerow(row)

        return response

    def test_func(self):
        event = get_object_or_404(Event, slug=self.kwargs["slug"])
        return self.request.user == event.organizer


class ManageRegistrationView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, registration_id):
        registration = get_object_or_404(Registration, id=registration_id)
        event = registration.event

        # Verify action
        action = request.POST.get("action")

        if action == "approve":
            # Check capacity before approving from waitlist/cancelled
            current_registrations = event.registrations.filter(
                status="registered"
            ).count()
            if current_registrations >= event.capacity:
                messages.error(request, "Cannot approve: Mission is at full capacity.")
            else:
                registration.status = "registered"
                registration.save()
                messages.success(
                    request,
                    f"Approved {registration.participant.username} for the mission.",
                )

                # Send email notification
                send_mail(
                    subject=f"Mission Status Update: APPROVED - {event.title}",
                    message=f"Commander {registration.participant.username},\n\nYour application for mission '{event.title}' has been APPROVED by the mission control (organizer).\n\nReport to the briefing room immediately.\n\n- Event Horizon Command",
                    from_email="command@eventhorizon.local",
                    recipient_list=[registration.participant.email],
                    fail_silently=True,
                )

        elif action == "waitlist":
            registration.status = "waitlisted"
            registration.save()
            messages.info(
                request, f"Moved {registration.participant.username} to standby list."
            )

            # Send email notification
            send_mail(
                subject=f"Mission Status Update: STANDBY - {event.title}",
                message=f"Commander {registration.participant.username},\n\nYou have been placed on the STANDBY list (waitlist) for mission '{event.title}'.\n\nAwait further instructions. We will notify you if a slot becomes available.\n\n- Event Horizon Command",
                from_email="command@eventhorizon.local",
                recipient_list=[registration.participant.email],
                fail_silently=True,
            )

        elif action == "cancel":
            registration.status = "cancelled"
            registration.save()
            messages.warning(
                request,
                f"Cancelled registration for {registration.participant.username}.",
            )

            # Send email notification
            send_mail(
                subject=f"Mission Status Update: CANCELLED - {event.title}",
                message=f"Commander {registration.participant.username},\n\nYour registration for mission '{event.title}' has been CANCELLED by mission control.\n\nIf you believe this is an error, contact the mission organizer directly.\n\n- Event Horizon Command",
                from_email="command@eventhorizon.local",
                recipient_list=[registration.participant.email],
                fail_silently=True,
            )

        return redirect("event-detail", slug=event.slug)

    def test_func(self):
        registration = get_object_or_404(
            Registration, id=self.kwargs["registration_id"]
        )
        return self.request.user == registration.event.organizer
