import threading
from django.views.decorators.cache import never_cache
import math
from urllib import request
from django.core.exceptions import ValidationError
from accounts.utils import send_vote_confirmation_email
from voting.models import Vote
from candidates.models import Candidate
from accounts.models import User
from elections.models import Election
from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import render
from voting.models import ElectionCandidate

# Create your views here.
@never_cache
def dashboard(request):

    user_id = request.session.get(
        "logged_in_user"
    )

    if not user_id:

        return redirect(
            "login"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    eligible_elections = Election.objects.filter(
        start_datetime__lte=timezone.now(),
        end_datetime__gte=timezone.now()
    ).filter(
        models.Q(
            election_type="CENTRAL"
        ) |
        models.Q(
            election_type="STATE",
            state=user.state
        )
    )
    user_votes = Vote.objects.filter(
        voter=user
    ).select_related(
        "election"
    )
    return render(
        request,
        "voting/dashboard.html",
        {
            "user": user,
            "eligible_elections": eligible_elections,
            "user_votes": user_votes
        }
    )
    
@never_cache
def election_detail(
    request,
    election_id
):

    user_id = request.session.get(
        "logged_in_user"
    )

    if not user_id:

        return redirect(
            "login"
        )
    election = get_object_or_404(
        Election,
        id=election_id
    )
    
    user = get_object_or_404(
        User,
        id=user_id
    )

    if (
        election.election_type == "STATE"
        and election.state != user.state
    ):

        return redirect(
            "dashboard"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    already_voted = Vote.objects.filter(
        voter=user,
        election=election
    ).exists()

    if already_voted:

        return render(
            request,
            "voting/already_voted.html",
            {
                "election": election
            }
        )

    election_candidates = (
        ElectionCandidate.objects
        .filter(
            election=election
        )
        .select_related(
            "candidate"
        )
    )
    if (
        request.session.get(
            "vote_election_id"
        ) != election.id
    ):

        request.session[
            "vote_start_time"
        ] = timezone.now().timestamp()

        request.session[
            "vote_election_id"
        ] = election.id
    remaining_time = get_remaining_time(
        request
    )
    if election.status != "ACTIVE":

        return render(
            request,
            "voting/election_inactive.html",
            {
                "election": election
            }
        )
    return render(
        request,
        "voting/election_detail.html",
        {
            "election": election,
            "election_candidates": election_candidates,
            "remaining_time":remaining_time
        }
    )
    
    
@never_cache
def vote_confirm(
    request,
    election_id,
    candidate_id
):

    user_id = request.session.get(
        "logged_in_user"
    )

    if not user_id:

        return redirect(
            "login"
        )

    election = get_object_or_404(
        Election,
        id=election_id
    )

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    remaining_time = get_remaining_time(
        request
    )

    if remaining_time <= 0:

        request.session.pop(
            "vote_start_time",
            None
        )

        request.session.pop(
            "vote_election_id",
            None
        )

        if remaining_time <= 0:

            request.session.flush()

            return redirect(
                "accounts:login"
            )
    return render(
        request,
        "voting/vote_confirm.html",
        {
            "election": election,
            "candidate": candidate,
            "remaining_time": remaining_time
        }
    )
    
def submit_vote(request):
    remaining = get_remaining_time(request)

    if remaining <= 0:

        request.session.pop(
            "vote_start_time",
            None
        )

        request.session.pop(
            "vote_election_id",
            None
        )

        if remaining <= 0:

            request.session.flush()

            return redirect(
                "accounts:login"
            )

    if request.method != "POST":

        return redirect(
            "dashboard"
        )

    user_id = request.session.get(
        "logged_in_user"
    )

    if not user_id:

        return redirect(
            "accounts:login"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    election_id = request.POST.get(
        "election_id"
    )

    candidate_id = request.POST.get(
        "candidate_id"
    )

    election = get_object_or_404(
        Election,
        id=election_id
    )

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    already_voted = Vote.objects.filter(
        voter=user,
        election=election
    ).exists()

    if already_voted:

        return render(
            request,
            "voting/already_voted.html"
        )

    

    try:

        vote = Vote(
            voter=user,
            election=election,
            candidate=candidate
        )

        vote.full_clean()
        vote.save()
        threading.Thread(
            target=
            send_vote_confirmation_email,
            args=(
                user,
                election
            )
        ).start()

    except ValidationError:

        return redirect(
            "dashboard"
        )
    
    
    request.session.pop(
        "vote_start_time",
        None
    )

    request.session.pop(
        "vote_election_id",
        None
    )
    if election.status != "ACTIVE":

        return render(
            request,
            "voting/election_inactive.html",
            {
                "election": election
            }
        )
    return redirect(
        "vote_success"
    )
    
@never_cache
def vote_success(request):

    return render(
        request,
        "voting/vote_success.html"
    )




def get_remaining_time(request):

    start_time = request.session.get(
        "vote_start_time"
    )

    if not start_time:
        return 0

    elapsed = (
        timezone.now().timestamp()
        - start_time
    )

    remaining = math.ceil(
        60 - elapsed
    )

    return max(
        remaining,
        0
    )