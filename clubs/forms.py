from django import forms
from clubs.models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
