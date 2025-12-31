from django.db import models
from django.conf import settings


class MembershipManager(models.Manager):
    def approved(self):
        return self.filter(status='APPROVED')
    
    def pending(self):
        return self.filter(status='PENDING')
    
    def for_club(self, club):
        return self.filter(club=club)
    
    def for_user(self, user):
        return self.filter(user=user)


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

    objects = MembershipManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'club']),
            models.Index(fields=['club', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
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
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN' and self.status == 'APPROVED'
    
    @property
    def is_moderator(self):
        return self.role in ['ADMIN', 'MODERATOR'] and self.status == 'APPROVED'
    
    @property
    def can_manage_posts(self):
        return self.is_moderator and self.status == 'APPROVED'