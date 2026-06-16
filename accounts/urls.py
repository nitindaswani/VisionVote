from django.urls import path

from . import views

urlpatterns = [

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "verify-registration-otp/",
        views.verify_registration_otp,
        name="verify_registration_otp"
    ),
    path(
        "registration-success/",
        views.registration_success,
        name="registration_success"
    ),
    
    path(
        "face-register/",
        views.face_register,
        name="face_register"
    ),

    path(
        "save-face/",
        views.save_face,
        name="save_face"
    ),
    path(
        "verify-blink/",
        views.verify_blink,
        name="verify_blink"
    ),
    path(
        "login/",
        views.login_view,
        name="login"
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
    path(
        "verify-login-otp/",
        views.verify_login_otp,
        name="verify_login_otp"
    ),
    path(
        "face-login/",
        views.face_login,
        name="face_login"
    ),
    path(
        "verify-face/",
        views.verify_face,
        name="verify_face"
    ),
]

app_name = "accounts"