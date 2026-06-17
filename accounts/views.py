import os

from django.views.decorators.cache import never_cache
from urllib import request
import requests
from django.db import models
from django.utils import timezone
from elections.models import Election
from django.core.mail import send_mail
from django.http import JsonResponse
import json
import base64
import cv2
import numpy as np
import face_recognition
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from .face_service import capture_face_encoding
from .models import FaceProfile
from .forms import OTPForm
from datetime import timedelta

from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail

from .forms import RegistrationForm
from .models import User, OTPVerification
from .utils import generate_otp
import threading
from django.core.mail import send_mail

def send_otp_email(email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Vision Vote",
            "email": "visionvote2026@gmail.com"
        },
        "to": [
            {
                "email": email
            }
        ],
        "subject": "Vision Vote OTP Verification",
        "textContent": f"Your OTP is {otp}. Valid for 5 minutes."
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print(response.status_code)
    print(response.text)


def send_voter_email(user):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Vision Vote",
            "email": "visionvote2026@gmail.com"
        },
        "to": [
            {
                "email": user.email
            }
        ],
        "subject": "Vision Vote Registration Successful",
        "textContent": (
            f"Dear {user.full_name},\n\n"
            f"Your Vision Vote account has been created successfully.\n\n"
            f"Your Voter ID is:\n"
            f"{user.voter_id}\n\n"
            f"Keep this Voter ID safe. "
            f"You will use it for login and voting."
        )
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print(response.status_code)
    print(response.text)    
    
def register_view(request):

    if request.method == "POST":

        form = RegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.is_verified = False
            user.save()

            otp = generate_otp()

            OTPVerification.objects.create(
                email=user.email,
                otp=otp,
                purpose="registration",
                expires_at=timezone.now() +
                timedelta(minutes=5)
            )

            threading.Thread(
                target=send_otp_email,
                args=(user.email, otp)
            ).start()

            request.session[
                "registration_user_id"
            ] = user.id

            return redirect(
                "accounts:verify_registration_otp"
            )

    else:

        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )
    
    
def verify_registration_otp(request):
    error_message = None

    user_id = request.session.get(
        "registration_user_id"
    )

    if not user_id:
        return redirect(
            "accounts:register"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    form = OTPForm()

    if request.method == "POST":

        form = OTPForm(
            request.POST
        )

        if form.is_valid():

            otp = form.cleaned_data["otp"]

            otp_record = OTPVerification.objects.filter(
                email=user.email,
                otp=otp,
                purpose="registration",
                is_used=False
            ).first()



            if request.method == "POST":

                form = OTPForm(request.POST)

                if form.is_valid():

                    otp = form.cleaned_data["otp"]

                    otp_record = OTPVerification.objects.filter(
                        email=user.email,
                        otp=otp,
                        purpose="registration",
                        is_used=False
                    ).first()

                    if not otp_record:

                        error_message = "Invalid OTP."

                    elif timezone.now() > otp_record.expires_at:

                        error_message = "OTP has expired."

                    else:

                        otp_record.is_used = True
                        otp_record.save()

                        user.is_verified = True
                        user.save()

                        request.session["face_user_id"] = user.id

                        return redirect("accounts:face_register")

    return render(
        request,
        "accounts/verify_registration_otp.html",
        {
            "form": form,
            "error_message": error_message
        }
    )
    
def registration_success(request):

    user_id = request.session.get(
        "registration_user_id"
    )

    if not user_id:
        return redirect("accounts:register")

    user = get_object_or_404(
        User,
        id=user_id
    )

    return render(
        request,
        "accounts/registration_success.html",
        {
            "voter_id": user.voter_id
        }
    )
    
    
def face_register(request):

    if not request.session.get("face_user_id"):
        return redirect("accounts:register")

    return render(
        request,
        "accounts/face_register.html"
    )
    
import time

@csrf_exempt
def save_face(request):
    start = time.time()
    print("START")
    if not request.session.get(
        "blink_verified"
    ):
        return JsonResponse({
            "success": False,
            "message": "Blink verification required"
        })
    if request.method != "POST":
        return JsonResponse(
            {"success": False}
        )
    print("Before encoding:", time.time() - start)
    user_id = request.session.get(
        "face_user_id"
    )

    if not user_id:

        return JsonResponse(
            {"success": False}
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    image_data = request.POST.get(
        "image"
    )

    image_data = image_data.split(
        ","
    )[1]

    image_bytes = base64.b64decode(
        image_data
    )

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )
    image = cv2.resize(
        image,
        (640, 480)
    )
    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    encodings = face_recognition.face_encodings(
        rgb
    )
    print("After encoding:", time.time() - start)
    if not encodings:

        return JsonResponse({
            "success": False,
            "message": "No face detected"
        })

    FaceProfile.objects.update_or_create(
        user=user,
        defaults={
            "face_encoding": json.dumps(
                encodings[0].tolist()
            )
        }
    )
    print("After DB save:", time.time() - start)
    threading.Thread(
        target=send_voter_email,
        args=(user,)
    ).start()
    print("After email:", time.time() - start)

    request.session.pop(
        "face_user_id",
        None
    )
    request.session.pop(
        "blink_verified",
        None
    )
    return JsonResponse({
        "success": True
    })



    
def verify_blink(request):

    request.session[
        "blink_verified"
    ] = True

    return JsonResponse({
        "success": True
    })

    
    
@never_cache    
def login_view(request):

    error_message = None

    if request.method == "POST":

        voter_id = request.POST.get(
            "voter_id"
        )

        user = User.objects.filter(
            voter_id=voter_id,
            is_verified=True,
            is_active=True
        ).first()

        if not user:

            error_message = (
                "Invalid Voter ID or account disabled."
            )

        else:

            otp = generate_otp()

            OTPVerification.objects.create(
                email=user.email,
                otp=otp,
                purpose="login",
                expires_at=
                timezone.now() +
                timedelta(minutes=5)
            )

            threading.Thread(
                target=send_otp_email,
                args=(user.email, otp)
            ).start()

            request.session[
                "login_user_id"
            ] = user.id

            return redirect(
                "accounts:verify_login_otp"
            )

    return render(
        request,
        "accounts/login.html",
        {
            "error_message":
            error_message
        }
    )
    
    
def logout_view(request):

    request.session.flush()

    return redirect(
        "accounts:login"
    )    
    
    
def face_login(request):

    return render(
        request,
        "accounts/face_login.html"
    )

    
def verify_login_otp(request):

    error_message = None

    user_id = request.session.get(
        "login_user_id"
    )

    if not user_id:
        return redirect(
            "accounts:login"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    form = OTPForm()

    if request.method == "POST":

        form = OTPForm(
            request.POST
        )

        if form.is_valid():

            otp = form.cleaned_data["otp"]

            otp_record = OTPVerification.objects.filter(
                email=user.email,
                otp=otp,
                purpose="login",
                is_used=False
            ).first()

            if not otp_record:

                error_message = (
                    "Invalid OTP."
                )

            elif timezone.now() > otp_record.expires_at:

                error_message = (
                    "OTP has expired."
                )

            else:

                otp_record.is_used = True
                otp_record.save()

                request.session[
                    "face_login_user_id"
                ] = user.id

                return redirect(
                    "accounts:face_login"
                )

    return render(
        request,
        "accounts/verify_login_otp.html",
        {
            "form": form,
            "error_message": error_message
        }
    )
    
@csrf_exempt
def verify_face(request):

    if not request.session.get(
        "blink_verified"
    ):
        return JsonResponse({
            "success": False,
            "message":
            "Blink verification required"
        })

    user_id = request.session.get(
        "face_login_user_id"
    )

    if not user_id:
        return JsonResponse({
            "success": False
        })

    user = get_object_or_404(
        User,
        id=user_id
    )

    image_data = request.POST.get(
        "image"
    )

    image_data = image_data.split(",")[1]

    image_bytes = base64.b64decode(
        image_data
    )

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    encodings = face_recognition.face_encodings(
        rgb
    )

    if not encodings:

        return JsonResponse({
            "success": False,
            "message":
            "No face detected"
        })

    current_encoding = encodings[0]

    stored_encoding = np.array(
        json.loads(
            user.face_profile.face_encoding
        )
    )

    result = face_recognition.compare_faces(
        [stored_encoding],
        current_encoding
    )[0]

    if not result:
        
        request.session.pop(
            "blink_verified",
            None
        )

        return JsonResponse({
            "success": False,
            "message":
            "Face verification failed"
        })

    request.session["logged_in_user"] = user.id

    request.session.pop(
        "vote_start_time",
        None
    )

    request.session.pop(
        "vote_election_id",
        None
    )

    request.session.pop(
        "face_login_user_id",
        None
    )

    request.session.pop(
        "blink_verified",
        None
    )

    return JsonResponse({
        "success": True
    })
    
    
    
