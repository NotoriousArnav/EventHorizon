import json

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone


def registration_status_label(status: str) -> str:
    if status == "registered":
        return "Approved"
    if status == "waitlisted":
        return "Waitlisted"
    if status == "cancelled":
        return "Not Approved"
    return status


def _normalize_answer(value):
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, indent=2, ensure_ascii=False)
    return str(value)


def _build_answer_items(*, event, answers):
    answers = answers or {}

    schema = event.registration_schema or []
    label_by_id = {}
    schema_ids = []

    for question in schema:
        if not isinstance(question, dict):
            continue
        q_id = question.get("id")
        if not q_id:
            continue
        schema_ids.append(q_id)
        label_by_id[q_id] = question.get("label") or q_id

    items = []

    if schema_ids:
        for q_id in schema_ids:
            if q_id not in answers:
                continue
            items.append(
                {
                    "id": q_id,
                    "label": label_by_id.get(q_id, q_id),
                    "value": _normalize_answer(answers.get(q_id)),
                }
            )

        # Answers present but not in schema
        for key in sorted(set(answers.keys()) - set(schema_ids)):
            items.append(
                {
                    "id": key,
                    "label": label_by_id.get(key, key),
                    "value": _normalize_answer(answers.get(key)),
                }
            )
    else:
        for key in sorted(answers.keys()):
            items.append(
                {
                    "id": key,
                    "label": label_by_id.get(key, key),
                    "value": _normalize_answer(answers.get(key)),
                }
            )

    return items


def _build_event_url(*, event, request):
    if request is None:
        return None
    if hasattr(request, "build_absolute_uri"):
        return request.build_absolute_uri(
            reverse("event-detail", kwargs={"slug": event.slug})
        )
    return None


def _send_email(*, subject, to_email, text_template, html_template, context):
    if not to_email:
        return

    text_body = render_to_string(text_template, context).strip()
    html_body = render_to_string(html_template, context)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@eventhorizon.local")
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)


def send_organizer_registration_email(*, registration, request=None):
    event = registration.event
    organizer_email = getattr(event.organizer, "email", "")
    if not organizer_email:
        return

    participant = registration.participant

    registered_at = registration.registered_at
    if registered_at and timezone.is_aware(registered_at):
        registered_at = timezone.localtime(registered_at)

    event_url = _build_event_url(event=event, request=request)

    current_site = Site.objects.get_current()

    answer_items = _build_answer_items(event=event, answers=registration.answers)
    answers_json = json.dumps(registration.answers or {}, indent=2, ensure_ascii=False)

    subject = f"New registration: {event.title}"

    context = {
        "current_site": current_site,
        "event": event,
        "event_url": event_url,
        "registration": registration,
        "status": registration.status,
        "registered_at": registered_at,
        "participant": participant,
        "answer_items": answer_items,
        "answers_json": answers_json,
    }

    _send_email(
        subject=subject,
        to_email=organizer_email,
        text_template="events/email/organizer_registration.txt",
        html_template="events/email/organizer_registration.html",
        context=context,
    )


def send_participant_registration_recorded_email(*, registration, request=None):
    participant_email = getattr(registration.participant, "email", "")
    if not participant_email:
        return

    event = registration.event
    current_site = Site.objects.get_current()

    event_url = _build_event_url(event=event, request=request)
    status_label = registration_status_label(registration.status)

    subject = f"Registration recorded: {event.title}"

    context = {
        "current_site": current_site,
        "event": event,
        "event_url": event_url,
        "registration": registration,
        "participant": registration.participant,
        "status": registration.status,
        "status_label": status_label,
    }

    _send_email(
        subject=subject,
        to_email=participant_email,
        text_template="events/email/participant_registration_recorded.txt",
        html_template="events/email/participant_registration_recorded.html",
        context=context,
    )


def send_participant_status_changed_email(
    *, registration, old_status: str, request=None
):
    participant_email = getattr(registration.participant, "email", "")
    if not participant_email:
        return

    event = registration.event
    current_site = Site.objects.get_current()

    event_url = _build_event_url(event=event, request=request)
    old_status_label = registration_status_label(old_status)
    new_status_label = registration_status_label(registration.status)

    subject = f"Mission status update: {event.title}"

    context = {
        "current_site": current_site,
        "event": event,
        "event_url": event_url,
        "registration": registration,
        "participant": registration.participant,
        "old_status": old_status,
        "new_status": registration.status,
        "old_status_label": old_status_label,
        "new_status_label": new_status_label,
    }

    _send_email(
        subject=subject,
        to_email=participant_email,
        text_template="events/email/participant_status_changed.txt",
        html_template="events/email/participant_status_changed.html",
        context=context,
    )
