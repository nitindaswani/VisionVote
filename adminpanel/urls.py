from django.urls import path
from adminpanel import views

urlpatterns = [
    
    path("",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "login/",
        views.admin_login,  name="admin_login"
    ),

    path(
        "login/",
        views.admin_login,
        name="admin_login"
    ),

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "logout/",
        views.admin_logout,
        name="admin_logout"
    ),
    path(
        "users/",
        views.manage_users,
        name="manage_users"
    ),
    path(
        "elections/",
        views.manage_elections,
        name="manage_elections"
    ),
    path(
        "elections/create/",
        views.create_election,
        name="create_election"
    ),
    path(
        "elections/edit/<int:election_id>/",
        views.edit_election,
        name="edit_election"
    ),
    path(
        "elections/delete/<int:election_id>/",
        views.delete_election,
        name="delete_election"
    ),
    path(
        "candidates/",
        views.manage_candidates,
        name="manage_candidates"
    ),
    path(
        "candidates/create/",
        views.create_candidate,
        name="create_candidate"
    ),
    path(
        "candidates/edit/<int:candidate_id>/",
        views.edit_candidate,
        name="edit_candidate"
    ),
    path(
        "candidates/delete/<int:candidate_id>/",
        views.delete_candidate,
        name="delete_candidate"
    ),
    path(
        "assign-candidate/",
        views.assign_candidate,
        name="assign_candidate"
    ),
    path(
        "users/toggle/<int:user_id>/",
        views.toggle_user_status,
        name="toggle_user_status"
    ),
]