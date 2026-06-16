from django.core.mail import send_mail
from django.utils import timezone
import random


def generate_otp():
    return str(
        random.randint(
            100000,
            999999
        )
    )
    
    


def send_vote_confirmation_email(
    user,
    election
):

    send_mail(
        subject=
        "Vision Vote - Vote Recorded",

        message=
        (
            f"Dear {user.full_name},\n\n"

            f"Your vote in the election:\n"
            f"{election.title}\n\n"

            f"has been successfully "
            f"recorded in Vision Vote.\n\n"

            f"Time: "
            f"{timezone.localtime().strftime('%d-%m-%Y %I:%M %p')}\n\n"

            f"Thank you for participating "
            f"in the democratic process.\n\n"

            f"Important:\n"
            f"Your vote remains secret."
        ),

        from_email=None,

        recipient_list=[
            user.email
        ]
    )