from django import forms
from datetime import date

from .models import User


class RegistrationForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'full_name',
            'email',
            'phone',
            'profile_picture',
            'dob',
            'address',
            'city',
            'state',
            'pincode',
            'aadhaar_number'
        ]

        widgets = {
            'dob': forms.DateInput(
                attrs={'type': 'date'}
            )
        }

    def clean_dob(self):

        dob = self.cleaned_data['dob']

        today = date.today()

        age = (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                <
                (dob.month, dob.day)
            )
        )

        if age < 18:

            raise forms.ValidationError(
                "You must be at least 18 years old to register."
            )

        return dob
    
    
    
class OTPForm(forms.Form):

    otp = forms.CharField(
        max_length=6
    )