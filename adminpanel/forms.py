from voting.models import ElectionCandidate
from django import forms
from candidates.models import Candidate
from django import forms
from elections.models import Election


class ElectionForm(forms.ModelForm):

    class Meta:

        model = Election

        fields = [

            "election_code",
            "title",
            "description",
            "election_type",
            "state",
            "election_cycle_years",
            "start_datetime",
            "end_datetime"

        ]

        widgets = {

            "start_datetime":
            forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),

            "end_datetime":
            forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),

        }
        
        


class CandidateForm(forms.ModelForm):

    class Meta:

        model = Candidate

        fields = [

            "name",
            "party_name",
            "party_logo",
            "slogan"

        ]
        
        
    


class ElectionCandidateForm(
    forms.ModelForm
):

    class Meta:

        model = ElectionCandidate

        fields = [

            "election",
            "candidate"

        ]