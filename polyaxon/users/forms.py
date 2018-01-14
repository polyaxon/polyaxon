# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import validate_slug

from libs.blacklist import validate_blacklist_name
from users import validators

User = get_user_model()


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        validators=[validate_slug, validate_blacklist_name])
    email = forms.EmailField(
        help_text='email address',
        required=True,
        validators=[
            validators.validate_new_email,
        ]
    )
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label="I have read and agree to the Terms of Service",
        error_messages={
            'required': "You must agree to the terms to register",
        }
    )
