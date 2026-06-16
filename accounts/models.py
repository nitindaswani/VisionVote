from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


INDIAN_STATES = [

    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),

    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli and Daman and Diu",
     "Dadra and Nagar Haveli and Daman and Diu"),
    ("Delhi", "Delhi"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),
    ("Ladakh", "Ladakh"),
    ("Lakshadweep", "Lakshadweep"),
    ("Puducherry", "Puducherry"),

]

class User(models.Model):

    voter_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/'
    )

    dob = models.DateField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100,
        choices=INDIAN_STATES
    )

    pincode = models.CharField(
        max_length=10
    )

    aadhaar_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='Aadhaar number must contain exactly 12 digits.'
            )
        ]
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.voter_id} - {self.full_name}"
    
    def save(self, *args, **kwargs):

        if not self.voter_id:

            year = datetime.now().year

            last_user = User.objects.order_by('-id').first()

            if last_user:
                next_id = last_user.id + 1
            else:
                next_id = 1

            self.voter_id = f"VV{year}{next_id:05d}"

        super().save(*args, **kwargs)    
    
    
class FaceProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='face_profile'
    )

    face_encoding = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.full_name
    
    def clean(self):

        if not self.face_encoding:
            raise ValidationError(
                "Face encoding cannot be empty."
            )
    
class OTPVerification(models.Model):

    PURPOSE_CHOICES = [
        ('registration', 'Registration'),
        ('login', 'Login'),
    ]

    email = models.EmailField()

    otp = models.CharField(
        max_length=6
    )

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.email} - {self.purpose}"
    
    
    