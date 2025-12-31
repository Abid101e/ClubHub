from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('BLOG', 'Blog'),
        ('NEWS', 'News'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    body = models.TextField()
    type = models.CharField(
        max_length=4,
        choices=POST_TYPE_CHOICES,
        default='BLOG'
    )
    club = models.ForeignKey(
        'clubs.Club',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['club', '-created_at']),
            models.Index(fields=['type', 'is_published']),
            models.Index(fields=['author']),
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})