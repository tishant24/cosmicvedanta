"""Authentication forms for email/mobile signup and login."""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

COSMIC_INPUT = 'cosmic-input'


class SignupForm(forms.ModelForm):
    """Registration form supporting email or mobile."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Create a password'}),
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Confirm password'}),
        label='Confirm Password',
    )

    class Meta:
        model = User
        fields = ['email', 'mobile', 'display_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Email address'}),
            'mobile': forms.TextInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Mobile number (with country code)'}),
            'display_name': forms.TextInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Display name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile = cleaned_data.get('mobile')
        if not email and not mobile:
            raise forms.ValidationError('Please provide either an email address or a mobile number.')
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Login form accepting email or mobile."""
    username = forms.CharField(
        label='Email or Mobile',
        widget=forms.TextInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Email or mobile number'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Password'}),
    )


class OTPVerifyForm(forms.Form):
    """OTP verification form."""
    otp_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': COSMIC_INPUT, 'placeholder': 'Enter 6-digit OTP'}),
    )
