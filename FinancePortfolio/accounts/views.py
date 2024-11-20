from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, LoginForm, ForgotPasswordForm
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib import messages

user = get_user_model()


# Create your views here.
def register_view(request):
    if request.POST == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("User from the form -----------", user)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration Successful. You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = user.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # keeps user logged in
            messages.success(request, "Password reset Successful. You can login with your new password.")
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})
