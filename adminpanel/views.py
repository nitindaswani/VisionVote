from adminpanel.forms import ElectionCandidateForm
from django.db import IntegrityError
from voting.models import Vote, ElectionCandidate
from django.contrib import messages
from adminpanel.forms import ElectionForm
from accounts.models import User
from elections.models import Election
from voting.models import Vote
from django.utils import timezone
from accounts.models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from elections.models import Election
from candidates.models import Candidate
from voting.models import Vote
from django.utils import timezone
from django.contrib import messages
from adminpanel.forms import CandidateForm


def admin_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_superuser:

            login(
                request,
                user
            )

            return redirect(
                "admin_dashboard"
            )

        error = "Invalid credentials"

    return render(
        request,
        "adminpanel/login.html",
        {
            "error": error
        }
    )


def admin_dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            "admin_login"
        )

    return render(
        request,
        "adminpanel/dashboard.html"
    )


def admin_logout(request):

    logout(request)

    return redirect(
        "admin_login"
    )
    
    
def admin_dashboard(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    context = {

        "total_users":
        User.objects.count(),

        "total_candidates":
        Candidate.objects.count(),

        "total_votes":
        Vote.objects.count(),

        "active_elections":
        Election.objects.filter(
            start_datetime__lte=
            timezone.now(),

            end_datetime__gte=
            timezone.now()
        ).count(),

        "ended_elections":
        Election.objects.filter(
            end_datetime__lt=
            timezone.now()
        ).count(),

        "total_elections":
        Election.objects.count(),

    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )
    
    
def manage_users(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    search = request.GET.get(
        "search",
        ""
    )

    users = User.objects.all()

    if search:

        users = users.filter(
            full_name__icontains=
            search
        )

    return render(
        request,
        "adminpanel/manage_users.html",
        {
            "users": users,
            "search": search
        }
    )
    
    
def manage_elections(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    elections = Election.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "adminpanel/manage_elections.html",
        {
            "elections": elections
        }
    )
    
    
def create_election(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    if request.method == "POST":

        form = ElectionForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "manage_elections"
            )

    else:

        form = ElectionForm()

    return render(
        request,
        "adminpanel/create_election.html",
        {
            "form": form
        }
    )
    
    
    
def edit_election(
    request,
    election_id
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if request.method == "POST":

        form = ElectionForm(
            request.POST,
            instance=election
        )

        if form.is_valid():

            form.save()

            return redirect(
                "manage_elections"
            )

    else:

        form = ElectionForm(
            instance=election
        )

    return render(
        request,
        "adminpanel/edit_election.html",
        {
            "form": form,
            "election": election
        }
    )
    
def delete_election(
    request,
    election_id
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if election.status == "ACTIVE":

        messages.error(
            request,
            "Active elections cannot be deleted."
        )

        return redirect(
            "manage_elections"
        )

    if Vote.objects.filter(
        election=election
    ).exists():

        messages.error(
            request,
            "Election with votes cannot be deleted."
        )

        return redirect(
            "manage_elections"
        )
    election.delete()

    return redirect(
        "manage_elections"
    )
    
    
    
def manage_candidates(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    candidates = Candidate.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "adminpanel/manage_candidates.html",
        {
            "candidates": candidates
        }
    )
    
    
def create_candidate(request):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    if request.method == "POST":

        form = CandidateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Candidate created successfully."
            )

            return redirect(
                "manage_candidates"
            )

    else:

        form = CandidateForm()

    return render(
        request,
        "adminpanel/create_candidate.html",
        {
            "form": form
        }
    )
    
    
def edit_candidate(
    request,
    candidate_id
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    if request.method == "POST":

        form = CandidateForm(
            request.POST,
            request.FILES,
            instance=candidate
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Candidate updated successfully."
            )

            return redirect(
                "manage_candidates"
            )

    else:

        form = CandidateForm(
            instance=candidate
        )

    return render(
        request,
        "adminpanel/edit_candidate.html",
        {
            "form": form,
            "candidate": candidate
        }
    )   
    
def delete_candidate(
    request,
    candidate_id
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    candidate = get_object_or_404(
        Candidate,
        id=candidate_id
    )

    if Vote.objects.filter(
        candidate=candidate
    ).exists():

        messages.error(
            request,
            "Candidate with votes cannot be deleted."
        )

        return redirect(
            "manage_candidates"
        )

    active_election_exists = (
        ElectionCandidate.objects.filter(
            candidate=candidate,
            election__start_datetime__lte=
            timezone.now(),
            election__end_datetime__gte=
            timezone.now()
        ).exists()
    )

    if active_election_exists:

        messages.error(
            request,
            "Candidate in active elections cannot be deleted."
        )

        return redirect(
            "manage_candidates"
        )

    candidate.delete()

    messages.success(
        request,
        "Candidate deleted successfully."
    )

    return redirect(
        "manage_candidates"
    )
    
    
def assign_candidate(
    request
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):

        return redirect(
            "admin_login"
        )

    if request.method == "POST":

        form = ElectionCandidateForm(
            request.POST
        )

        if form.is_valid():

            try:

                form.save()

                messages.success(
                    request,
                    "Candidate assigned successfully."
                )

                return redirect(
                    "assign_candidate"
                )

            except IntegrityError:

                messages.error(
                    request,
                    "Candidate already assigned to this election."
                )

    else:

        form = ElectionCandidateForm()

    return render(
        request,
        "adminpanel/assign_candidate.html",
        {
            "form": form
        }
    )
    
    
    


def toggle_user_status(
    request,
    user_id
):

    if (
        not request.user.is_authenticated
        or
        not request.user.is_superuser
    ):
        return redirect(
            "admin_login"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    user.is_active = (
        not user.is_active
    )

    user.save()

    messages.success(
        request,
        "User status updated."
    )

    return redirect(
        "manage_users"
    )