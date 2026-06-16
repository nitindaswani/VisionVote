from django.urls import path
from results import views

urlpatterns = [

    path(
        "",
        views.results_home,
        name="results_home"
    ),

    path(
        "<int:election_id>/",
        views.election_results,
        name="election_results"
    ),
    path(
        "export/<int:election_id>/",
        views.export_results_csv,
        name="export_results_csv"
    ),

]