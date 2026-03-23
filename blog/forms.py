"""Blog forms for comments and user submissions."""
from django import forms
from .models import Comment, UserPost


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


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'rows': 3,
            }),
        }


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['title', 'category', 'body', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Your post title...',
            }),
            'category': forms.Select(attrs={
                'class': 'cosmic-input',
            }),
            'body': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Write your thoughts, insights, discoveries...',
                'rows': 10,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'cosmic-input',
            }),
        }
