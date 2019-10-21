from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UsernameField
from django.core.validators import validate_slug

import ownership

from api.users import validators
from libs.blacklist import validate_blacklist_name


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        validators=[validate_slug, validate_blacklist_name, ownership.validate_owner_name])
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    email = forms.EmailField(
        help_text='email address',
        required=True,
        validators=[
            validators.validate_new_email,
        ]
    )
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='I have read and agree to the Terms of Service',
        error_messages={
            'required': "You must agree to the terms to register",
        }
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
