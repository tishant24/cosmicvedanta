"""Blog forms for comments and user submissions."""
from django import forms
from .models import Comment, UserPost, Post


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


class AdminPostForm(forms.ModelForm):
    """Full post form for admin — publishes directly."""
    class Meta:
        model = Post
        fields = ['title', 'category', 'body', 'featured_image', 'excerpt',
                  'vedanta_quote', 'vedanta_source', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Post title...',
            }),
            'category': forms.Select(attrs={
                'class': 'cosmic-input',
            }),
            'body': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Write in plain text — auto-formats to beautiful HTML...',
                'rows': 15,
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Short summary (auto-generated if blank)...',
                'rows': 3,
            }),
            'vedanta_quote': forms.Textarea(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Optional philosophical quote...',
                'rows': 3,
            }),
            'vedanta_source': forms.TextInput(attrs={
                'class': 'cosmic-input',
                'placeholder': 'Quote source (e.g., Upanishads)...',
            }),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'cosmic-input',
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
