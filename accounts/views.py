"""Account views: signup, login, logout, OTP verification."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignupForm, LoginForm, OTPVerifyForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailOrMobileBackend')
            messages.success(request, 'Welcome to CosmicVedanta! Your journey begins now.')
            return redirect('blog:home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user, backend='accounts.backends.EmailOrMobileBackend')
                next_url = request.GET.get('next', 'blog:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you among the stars!')
    return redirect('blog:home')


def otp_verify_view(request):
    """Placeholder for OTP verification flow."""
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.is_authenticated and user.verify_otp(form.cleaned_data['otp_code']):
                messages.success(request, 'Mobile number verified successfully!')
                return redirect('blog:home')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
    else:
        form = OTPVerifyForm()
        # In production, trigger OTP send here:
        # request.user.generate_otp()
        # send_sms(request.user.mobile, otp_code)
    return render(request, 'accounts/otp_verify.html', {'form': form})
