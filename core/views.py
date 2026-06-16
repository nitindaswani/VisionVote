from django.shortcuts import render
from elections.models import Election
from django.utils import timezone


def home(request):

    election_type = request.GET.get(
        "type"
    )

    state = request.GET.get(
        "state"
    )

    active_elections = Election.objects.filter(
        start_datetime__lte=timezone.now(),
        end_datetime__gte=timezone.now()
    )

    upcoming_elections = Election.objects.filter(
        start_datetime__gt=timezone.now()
    )

    if election_type:

        upcoming_elections = (
            upcoming_elections.filter(
                election_type=election_type
            )
        )

    if state:

        upcoming_elections = (
            upcoming_elections.filter(
                state=state
            )
        )

    states = (
        Election.objects
        .exclude(
            state__isnull=True
        )
        .exclude(
            state=""
        )
        .values_list(
            "state",
            flat=True
        )
        .distinct()
        .order_by(
            "state"
        )
    )

    return render(
        request,
        "core/home.html",
        {
            "active_elections": active_elections,
            "upcoming_elections": upcoming_elections,
            "states": states
        }
    )