# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from registration import validators

User = get_user_model()


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        help_text='email address',
        required=True,
        validators=[
            validators.validate_confusables_email,
        ]
    )
    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label="I have read and agree to the Terms of Service",
        error_messages={
            'required': validators.TOS_REQUIRED,
        }
    )
