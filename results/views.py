from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from elections.models import Election
from voting.models import Vote
from django.db.models import Count
from django.utils import timezone
import csv
from django.http import HttpResponse


def results_home(request):

    ended_elections = Election.objects.filter(
        end_datetime__lt=timezone.now()
    )

    back_url = request.META.get('HTTP_REFERER', '/')
    return render(
        request,
        "results/results_home.html",
        {
            "ended_elections": ended_elections,
            "back_url": back_url
        }
    )


def election_results(
    request,
    election_id
):

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if election.status != "ENDED":

        return render(
            request,
            "results/results_hidden.html",
            {
                "election": election
            }
        )

    results = (
        Vote.objects
        .filter(
            election=election
        )
        .values(
            "candidate__name",
            "candidate__party_name"
        )
        .annotate(
            total_votes=Count("id")
        )
        .order_by(
            "-total_votes"
        )
    )
    total_votes = Vote.objects.filter(
        election=election
    ).count()

    for result in results:

        if total_votes > 0:

            result["percentage"] = round(
                (result["total_votes"] / total_votes) * 100,
                2
            )

        else:

            result["percentage"] = 0
    winner = None

    if results:

        winner = results[0]
        
    back_url = request.META.get('HTTP_REFERER', '/')
    return render(
        request,
        "results/election_results.html",
        {
            "election": election,
            "results": results,
            "winner": winner,
            "total_votes": total_votes,
            "back_url": back_url
        }
    )
    
    
    
    
def export_results_csv(
    request,
    election_id
):

    election = get_object_or_404(
        Election,
        id=election_id
    )

    if election.status != "ENDED":

        return redirect(
            "results_home"
        )

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="{election.title}.csv"'
    )

    writer = csv.writer(
        response
    )

    writer.writerow([
        "Candidate",
        "Party",
        "Votes",
        "Percentage"
    ])

    results = (
        Vote.objects
        .filter(
            election=election
        )
        .values(
            "candidate__name",
            "candidate__party_name"
        )
        .annotate(
            total_votes=Count("id")
        )
        .order_by(
            "-total_votes"
        )
    )

    total_votes = Vote.objects.filter(
        election=election
    ).count()

    for result in results:

        percentage = 0

        if total_votes > 0:

            percentage = round(
                (
                    result["total_votes"]
                    / total_votes
                ) * 100,
                2
            )

        writer.writerow([
            result["candidate__name"],
            result["candidate__party_name"],
            result["total_votes"],
            percentage
        ])

    return response