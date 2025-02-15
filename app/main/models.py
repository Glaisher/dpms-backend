from django.db import models
from accounts.models import User
import uuid
from datetime import datetime


class Permit(models.Model):
    PERMIT_TYPES = [
        ('Restricted', 'Restricted'),
        ('Temporary', 'Temporary'),
        ('Permanent', 'Permanent'),
    ]

    PERMIT_STATUSES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Invalid', 'Invalid'),
    ]

    employee = models.ForeignKey(User, on_delete=models.PROTECT)
    permit_type = models.CharField(max_length=20, choices=PERMIT_TYPES)
    valid_from = models.DateField()
    valid_until = models.DateField()
    justification = models.TextField()
    status = models.CharField(max_length=20, default='Pending', choices=PERMIT_STATUSES)
    qr_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return self.valid_until < datetime.today().date()

    @property
    def permit_status(self):
        if self.status == 'Approved' and not self.is_expired():
            return 'active'
        if self.is_expired():
            return 'expired'
        return 'invalid'

    def __str__(self):
        return f"Permit for {self.employee.employee_id} - {self.permit_type}"

    class Meta:
        ordering = ['-created_at']


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('verified', 'Verified'),
    ]

    permit = models.ForeignKey(Permit, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()}"

    class Meta:
        ordering = ['-timestamp']
