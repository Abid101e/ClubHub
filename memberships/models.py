from django.db import models
from django.conf import settings


class Membership(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator'),
        ('MEMBER', 'Member'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='membership_set'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'club']),
            models.Index(fields=['club', 'status']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'club'],
                condition=models.Q(status='PENDING'),
                name='unique_pending_membership'
            )
        ]
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'

    def __str__(self):
        return f"{self.user.username} - {self.club.name} ({self.get_role_display()})"