from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import INDIAN_STATES

class Election(models.Model):

    ELECTION_TYPES = (
        ('CENTRAL', 'Central'),
        ('STATE', 'State'),
    )

    election_code = models.CharField(
        max_length=50,
        unique=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    election_type = models.CharField(
        max_length=20,
        choices=ELECTION_TYPES
    )

 
    state = models.CharField(
        max_length=100,
        choices=INDIAN_STATES,
        blank=True,
        null=True
    )

    election_cycle_years = models.PositiveIntegerField(
        default=5
    )

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def status(self):

        now = timezone.now()

        if now < self.start_datetime:
            return "UPCOMING"

        elif self.start_datetime <= now <= self.end_datetime:
            return "ACTIVE"

        return "ENDED"

    def __str__(self):
        return self.title
    
    
    def clean(self):

        if self.election_type == 'STATE' and not self.state:
            raise ValidationError(
                "State is required for state elections."
            )

        if self.end_datetime <= self.start_datetime:
            raise ValidationError(
                "End date must be greater than start date."
            )
            
    def save(self, *args, **kwargs):

        self.election_code = self.election_code.upper()

        super().save(*args, **kwargs)