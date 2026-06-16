from django.db import models
from django.core.exceptions import ValidationError
from elections.models import Election
from candidates.models import Candidate


class ElectionCandidate(models.Model):

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='election_candidates'
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='candidate_elections'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'election',
            'candidate'
        )

    def __str__(self):
        return f"{self.candidate.name} - {self.election.title}"
    
    
    
from accounts.models import User


class Vote(models.Model):

    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes'
    )

    voted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['voter', 'election'],
                name='one_vote_per_election'
            )
        ]

    def __str__(self):
        return f"{self.voter.full_name} -> {self.candidate.name}"
    
    def clean(self):

        from voting.models import ElectionCandidate

        valid_candidate = ElectionCandidate.objects.filter(
            election=self.election,
            candidate=self.candidate
        ).exists()

        if not valid_candidate:
            raise ValidationError(
                "Candidate does not belong to this election."
            )