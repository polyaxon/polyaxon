from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from libs.string_utils import strip_spaces


def render_mail_template(subject_template, body_template, context):
    """
    Renders both the subject and body templates in the given context.
    Returns a tuple (subject, body) of the result.
    """
    try:
        subject = strip_spaces(render_to_string(subject_template, context))
        body = render_to_string(body_template, context)
    finally:
        pass

    return subject, body


def send_mass_template_mail(subject_template, body_template, recipients, context=None):
    """
    Renders an email subject and body using the given templates and context,
    then sends it to the given recipients list.

    The emails are send one-by-one.
    """
    if context:
        subject, body = render_mail_template(subject_template, body_template, context)
    else:
        subject, body = subject_template, body_template

    message_tuples = [(subject, body, settings.DEFAULT_FROM_EMAIL, [r]) for r in recipients]

    send_mass_mail(message_tuples)


def send_mass_user_template_mail(subject_template, body_template, users, context):
    """
    Similar to `send_mass_template_mail` this function renders the given templates
    into email subjects and bodies.

    The emails are send one-by-one.
    """
    message_tuples = []
    for user in users:
        context['user'] = user
        subject, body = render_mail_template(subject_template, body_template, context)

        message_tuples.append((subject, body, settings.DEFAULT_FROM_EMAIL, [user.email]))

    if message_tuples:
        send_mass_mail(message_tuples)
