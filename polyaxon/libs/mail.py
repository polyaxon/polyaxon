from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string


def simplify(value):
    """
    Simplifies a string by removing leading and trailing whitespaces.
    Replaces also multiple whitespaces within the string with a single space.
    """
    return ' '.join(value.strip().split())


def render_mail_template(subject_template, body_template, context):
    """
    Renders both the subject and body templates in the given context.
    Returns a tuple (subject, body) of the result.
    """
    try:
        subject = simplify(render_to_string(subject_template, context))
        body = render_to_string(body_template, context)
    finally:
        pass

    return subject, body


def send_template_mail(subject_template, body_template, context, recipients):
    """
    Renders an email subject and body using the given templates and context,
    then sends it to the given recipients list.
    """
    subject, body = render_mail_template(subject_template, body_template, context)

    # send resulting emails
    send_bulk_mail(subject, body, recipients)


def send_bulk_mail(subject, body, recipients):
    """
    Sends an email with the given subject and body to every recipient in the
    set/list of recipients. The emails are send one-by-one (so that no
    addresses are "leaked", e.g. by putting all receivers in the "TO: " field).

    The sender email address is read from the settings.
    """

    message_tuples = [(subject, body, settings.DEFAULT_FROM_EMAIL, [r])
                      for r in recipients]

    send_mass_mail(message_tuples)


def send_bulk_template_mail(subject_template, body_template, context, users):
    """
    Similar to `send_template_mail` this function renders the given templates
    into email subjects and bodies.

    The resulting messages are collected and then sent at once using
    `send_mass_mail`.
    """
    messages = []
    for user in users:
        context['user'] = user
        subject, body = render_mail_template(subject_template, body_template, context)

        messages.append((subject, body, None, [user.email]))

    if messages:
        send_mass_mail(messages)
