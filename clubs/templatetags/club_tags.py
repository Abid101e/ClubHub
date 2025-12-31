from django import template

register = template.Library()


@register.simple_tag
def user_role_in_club(user, club):
    if not user.is_authenticated:
        return None
    membership = club.membership_set.filter(user=user, status='APPROVED').first()
    return membership.role if membership else None


@register.filter
def can_create_news(user, club):
    role = user_role_in_club(user, club)
    return role in ['ADMIN', 'MODERATOR']


@register.filter
def can_create_post(user, club):
    role = user_role_in_club(user, club)
    return role in ['ADMIN', 'MODERATOR', 'MEMBER']
