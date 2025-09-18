from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )

User = get_user_model()

# -------- Security phrase + forgot password forms (no questions) --------

class SecurityPhraseForm(forms.Form):
    phrase = forms.CharField(
        label="Security phrase",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    confirm_phrase = forms.CharField(
        label="Confirm security phrase",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('error_class', CustomErrorList)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('phrase') != cleaned.get('confirm_phrase'):
            raise forms.ValidationError("Phrases do not match.")
        return cleaned

class ForgotPasswordStartForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('error_class', CustomErrorList)
        super().__init__(*args, **kwargs)

class ForgotPasswordVerifyForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput())
    phrase = forms.CharField(
        label="Security phrase",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('error_class', CustomErrorList)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned