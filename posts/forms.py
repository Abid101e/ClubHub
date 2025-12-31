from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'type']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, user_role=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_role == 'MEMBER':
            self.fields['type'].choices = [('BLOG', 'Blog')]
            self.fields['type'].initial = 'BLOG'
        elif user_role in ['MODERATOR', 'ADMIN']:
            self.fields['type'].choices = Post.POST_TYPE_CHOICES
