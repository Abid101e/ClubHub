from django.db.models.signals import post_save
from django.dispatch import receiver
from clubs.models import Club
from memberships.models import Membership


@receiver(post_save, sender=Club)
def create_admin_membership(sender, instance, created, **kwargs):
    if created:
        Membership.objects.create(
            user=instance.creator,
            club=instance,
            role='ADMIN',
            status='APPROVED'
        )