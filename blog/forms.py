"""Blog forms for comments."""
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Share your thoughts on the cosmos...',
                'rows': 4,
            }),
        }
