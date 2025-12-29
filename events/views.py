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
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .models import Event, Registration, Webhook
from .notifications import (
    send_organizer_registration_email,
    send_participant_registration_recorded_email,
    send_participant_status_changed_email,
)
from .utils import extract_registration_schema
from .webhook_utils import trigger_webhook_async


def _trigger_registration_created_webhooks(
    *, event, registration, participant, answers
):
    webhooks = event.webhooks.filter(is_active=True)
    if not webhooks.exists():
        return

    payload = {
        "event": "registration.created",
        "mission_id": event.slug,
        "mission_title": event.title,
        "participant": {
            "username": participant.username,
            "email": getattr(participant, "email", ""),
        },
        "status": registration.status,
        "registered_at": registration.registered_at,
        "answers": answers,
    }

    for webhook in webhooks:
        trigger_webhook_async(webhook.url, payload)


def _trigger_registration_status_changed_webhooks(
    *, event, registration, participant, old_status, new_status
):
    webhooks = event.webhooks.filter(is_active=True)
    if not webhooks.exists():
        return

    payload = {
        "event": "registration.status_changed",
        "mission_id": event.slug,
        "mission_title": event.title,
        "participant": {
            "username": participant.username,
            "email": getattr(participant, "email", ""),
        },
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": timezone.now(),
    }

    for webhook in webhooks:
        trigger_webhook_async(webhook.url, payload)


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"
    ordering = ["start_time"]
    paginate_by = 6

    def get_queryset(self):
        """
        Return the Event queryset filtered by optional `q` (title or description) and `location` GET parameters, with `organizer` and `organizer.profile` preloaded.
        
        Filters:
        - `q`: case-insensitive substring match against `title` or `description`.
        - `location`: case-insensitive substring match against `location`.
        
        Returns:
            QuerySet: Event objects matching the provided filters with `organizer` and `organizer.profile` selected for eager loading.
        """
        queryset = (
            super().get_queryset().select_related("organizer", "organizer__profile")
        )
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
        context["current_query"] = self.request.GET.get("q", "")
        context["current_location"] = self.request.GET.get("location", "")
        return context


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/user_events.html"
    context_object_name = "hosted_events"

    def get_queryset(self):
        """
        Retrieve the current user's events with organizer and organizer profile eager-loaded, ordered by start_time.
        
        Returns:
            QuerySet[Event]: Events organized by the request's user with `organizer` and `organizer__profile` selected and ordered by `start_time`.
        """
        return (
            Event.objects.filter(organizer=self.request.user)
            .select_related("organizer", "organizer__profile")
            .order_by("start_time")
        )

    def get_context_data(self, **kwargs):
        """
        Add the current user's registrations to the template context under the key "attended_registrations".
        
        The value is a queryset of Registration objects for the requesting user, eager-loading related event and organizer (including organizer profile) and ordered by the related event's start_time.
        
        Returns:
            context (dict): Template context including "attended_registrations".
        """
        context = super().get_context_data(**kwargs)
        context["attended_registrations"] = (
            Registration.objects.filter(participant=self.request.user)
            .select_related("event", "event__organizer", "event__organizer__profile")
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

        context["webhooks"] = event.webhooks.order_by("-created_at")

        if user.is_authenticated:
            user_registration = Registration.objects.filter(
                event=event, participant=user
            ).first()

            context["is_registered"] = user_registration is not None
            context["user_registration"] = user_registration

            if user == event.organizer:
                context["registrations"] = (
                    Registration.objects.filter(event=event)
                    .select_related("participant", "participant__profile")
                    .order_by("-registered_at")
                )
        else:
            context["is_registered"] = False

        return context


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time", "location", "capacity"]
    template_name = "events/event_form.html"
    success_message = "Event '%(title)s' was created successfully"

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
        return self.request.user == event.organizer

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
        return self.request.user == event.organizer


class EventRegistrationView(LoginRequiredMixin, View):
    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        if Registration.objects.filter(event=event, participant=request.user).exists():
            messages.warning(request, "You are already registered for this mission.")
            return redirect("event-detail", slug=slug)

        answers = {}
        if event.registration_schema:
            for question in event.registration_schema:
                key = f"answer_{question['id']}"
                if question.get("type") == "checkbox":
                    answers[question["id"]] = request.POST.get(key) == "on"
                else:
                    answers[question["id"]] = request.POST.get(key, "")

        current_registrations = event.registrations.filter(status="registered").count()

        if current_registrations >= event.capacity:
            status_value = "waitlisted"
            msg_type = messages.INFO
            msg_text = "Mission capacity reached. You have been placed on the standby (wait) list."
        else:
            status_value = "registered"
            msg_type = messages.SUCCESS
            msg_text = f"Successfully registered for mission: {event.title}"

        registration = Registration.objects.create(
            event=event, participant=request.user, status=status_value, answers=answers
        )

        if msg_type == messages.INFO:
            messages.info(request, msg_text)
        else:
            messages.success(request, msg_text)

        send_organizer_registration_email(registration=registration, request=request)
        send_participant_registration_recorded_email(
            registration=registration, request=request
        )

        _trigger_registration_created_webhooks(
            event=event,
            registration=registration,
            participant=request.user,
            answers=answers,
        )

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


class EventExportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{event.slug}_roster.csv"'
        )

        writer = csv.writer(response)

        headers = ["Username", "Email", "Status", "Registered At"]

        question_ids = []
        if event.registration_schema:
            for question in event.registration_schema:
                headers.append(question["label"])
                question_ids.append(question["id"])

        writer.writerow(headers)

        registrations = event.registrations.select_related("participant").all()
        for reg in registrations:
            row = [
                reg.participant.username,
                reg.participant.email,
                reg.status,
                reg.registered_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]

            if event.registration_schema:
                for q_id in question_ids:
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

        action = request.POST.get("action")
        old_status = registration.status

        if action == "approve":
            current_registrations = event.registrations.filter(
                status="registered"
            ).count()
            if current_registrations >= event.capacity:
                messages.error(request, "Cannot approve: Mission is at full capacity.")
                return redirect("event-detail", slug=event.slug)

            registration.status = "registered"
            registration.save()
            messages.success(
                request,
                f"Approved {registration.participant.username} for the mission.",
            )

        elif action == "waitlist":
            registration.status = "waitlisted"
            registration.save()
            messages.info(
                request, f"Moved {registration.participant.username} to standby list."
            )

        elif action == "cancel":
            registration.status = "cancelled"
            registration.save()
            messages.warning(
                request,
                f"Updated status for {registration.participant.username} to Not Approved.",
            )

        if registration.status != old_status:
            send_participant_status_changed_email(
                registration=registration, old_status=old_status, request=request
            )
            _trigger_registration_status_changed_webhooks(
                event=event,
                registration=registration,
                participant=registration.participant,
                old_status=old_status,
                new_status=registration.status,
            )

        return redirect("event-detail", slug=event.slug)

    def test_func(self):
        registration = get_object_or_404(
            Registration, id=self.kwargs["registration_id"]
        )
        return self.request.user == registration.event.organizer


class WebhookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Webhook
    fields = ["url", "secret", "is_active"]
    template_name = "events/webhook_form.html"

    def get_event(self):
        return get_object_or_404(Event, slug=self.kwargs["slug"])

    def test_func(self):
        event = self.get_event()
        return self.request.user == event.organizer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_event()
        context["is_create"] = True
        return context

    def form_valid(self, form):
        form.instance.event = self.get_event()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("event-detail", kwargs={"slug": self.get_event().slug})


class WebhookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Webhook
    fields = ["url", "secret", "is_active"]
    template_name = "events/webhook_form.html"

    def test_func(self):
        webhook = self.get_object()
        return self.request.user == webhook.event.organizer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.object.event
        context["is_create"] = False
        return context

    def get_success_url(self):
        return reverse("event-detail", kwargs={"slug": self.object.event.slug})


class WebhookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Webhook
    template_name = "events/webhook_confirm_delete.html"

    def test_func(self):
        webhook = self.get_object()
        return self.request.user == webhook.event.organizer

    def get_success_url(self):
        return reverse("event-detail", kwargs={"slug": self.object.event.slug})


class WebhookToggleActiveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        webhook = get_object_or_404(Webhook, pk=pk)
        webhook.is_active = not webhook.is_active
        webhook.save(update_fields=["is_active"])
        return redirect("event-detail", slug=webhook.event.slug)

    def test_func(self):
        webhook = get_object_or_404(Webhook, pk=self.kwargs["pk"])
        return self.request.user == webhook.event.organizer