from django.urls import path
from voting import views

urlpatterns = [

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "election/<int:election_id>/",
        views.election_detail,
        name="election_detail"
    ),

    path(
        "vote-confirm/<int:election_id>/<int:candidate_id>/",
        views.vote_confirm,
        name="vote_confirm"
    ),

    path(
        "submit-vote/",
        views.submit_vote,
        name="submit_vote"
    ),

    path(
        "vote-success/",
        views.vote_success,
        name="vote_success"
    ),

]