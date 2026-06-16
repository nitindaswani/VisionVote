from django.db import models


class Candidate(models.Model):

    candidate_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    party_name = models.CharField(
        max_length=200
    )

    party_logo = models.ImageField(
        upload_to='party_logos/'
    )

    slogan = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} ({self.party_name})"
    
    def save(self, *args, **kwargs):

        if not self.candidate_id:

            last_candidate = Candidate.objects.order_by('-id').first()

            if last_candidate:
                next_id = last_candidate.id + 1
            else:
                next_id = 1

            self.candidate_id = f"CAND{next_id:05d}"

        super().save(*args, **kwargs)