from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# keep your original views exactly
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username/password is incorrect.'
            return render(request, 'accounts/login.html',
                          {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})


# ----------------------------------------------------------------------
# Security-phrase + forgot-password views (append below your originals)
# ----------------------------------------------------------------------
from django.contrib import messages
from django.urls import reverse
from .models import UserSecurityPhrase
from .forms import SecurityPhraseForm, ForgotPasswordStartForm, ForgotPasswordVerifyForm

@login_required
def security_settings(request):
    template_data = {'title': 'Security Settings'}
    current = getattr(request.user, "security_phrase", None)

    if request.method == 'POST':
        form = SecurityPhraseForm(request.POST)
        if form.is_valid():
            sp = current or UserSecurityPhrase(user=request.user)
            sp.set_phrase(form.cleaned_data['phrase'])
            sp.save()
            template_data['success'] = 'Security phrase saved.'
            template_data['form'] = SecurityPhraseForm()  # reset
        else:
            template_data['form'] = form
    else:
        template_data['form'] = SecurityPhraseForm()

    template_data['has_phrase'] = bool(current)
    return render(request, 'accounts/security_settings.html', {'template_data': template_data})


def forgot_password_start(request):
    template_data = {'title': 'Forgot Password'}
    if request.method == 'POST':
        form = ForgotPasswordStartForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            if not user:
                template_data['error'] = 'No user with that username.'
                template_data['form'] = form
            elif not hasattr(user, 'security_phrase'):
                template_data['error'] = 'This account does not have a security phrase set.'
                template_data['form'] = form
            else:
                url = reverse('accounts.forgot_password_verify') + f'?username={user.username}'
                return redirect(url)
        else:
            template_data['form'] = form
    else:
        template_data['form'] = ForgotPasswordStartForm()

    return render(request, 'accounts/forgot_password_start.html', {'template_data': template_data})


def forgot_password_verify(request):
    username = request.GET.get('username') or request.POST.get('username')
    user = User.objects.filter(username=username).first()
    if not user:
        return redirect('accounts.forgot_password_start')

    sp = getattr(user, 'security_phrase', None)
    if not sp:
        return redirect('accounts.forgot_password_start')

    template_data = {'title': 'Verify Identity'}

    if request.method == 'POST':
        form = ForgotPasswordVerifyForm(request.POST)
        if form.is_valid():
            if not sp.check_phrase(form.cleaned_data['phrase']):
                template_data['error'] = 'Incorrect security phrase.'
                template_data['form'] = form
            else:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, "Password reset. You can now log in.")
                return redirect('accounts.login')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = ForgotPasswordVerifyForm(initial={'username': username})

    return render(request, 'accounts/forgot_password_verify.html', {'template_data': template_data})
