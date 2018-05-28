import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from libs.utils import to_bool

_logger = logging.getLogger('polyaxon.commands')


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    """Management utility to create users/superusers.

    This is command is different than the django one, because:
        1. does not prompt the user to enter a password, i.e. can be used inline.
        2. validates and requires an email.
    """
    help = 'Used to create a user/superuser.'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        # pylint:disable= protected-access
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)
        # pylint:disable= protected-access
        self.email_field = self.UserModel._meta.get_field('email')

    def add_arguments(self, parser):
        parser.add_argument(
            '--%s' % self.UserModel.USERNAME_FIELD,
            required=True,
            dest=self.UserModel.USERNAME_FIELD,
            help='Specifies the login for the user/superuser.',
        )
        parser.add_argument(
            '--password',
            required=True,
            dest='password',
            help='Specifies the pasword for the user/superuser.',
        )
        parser.add_argument(
            '--email',
            required=True,
            dest='email',
            help='Specifies the email for the user/superuser.',
        )
        parser.add_argument(
            '--superuser',
            dest='is_superuser',
            action="store_true",
            default=False,
            help='Specifies a user or superuser.',
        )
        parser.add_argument(
            '--force',
            dest='force',
            action="store_true",
            default=False,
            help='To force create the user even if the user is not valid.',
        )

    def validate_password(self, password, user_data, force):
        try:
            validate_password(password, self.UserModel(**user_data))
        except ValidationError as e:
            _logger.warning('The password provided is not valid %s', e)
            if force:
                _logger.warning(
                    'The user will be created although the password does not meet the validation.')
            else:
                raise e

    def handle(self, *args, **options):  # pylint:disable=too-many-branches
        username = options[self.UserModel.USERNAME_FIELD].strip()
        password = options['password'].strip()
        email = options['email'].strip()
        force = to_bool(options['force'])
        is_superuser = to_bool(options['is_superuser'])

        try:
            username = self.username_field.clean(username, None)
        except exceptions.ValidationError as e:
            raise CommandError('; '.join(e.messages))

        try:
            self.email_field.clean(email, None)
        except exceptions.ValidationError as e:
            raise CommandError('; '.join(e.messages))

        try:
            self.UserModel.objects.get_by_natural_key(username)
        except self.UserModel.DoesNotExist:
            pass
        else:
            raise CommandError("Error: That username {} is already taken.".format(username))

        try:
            self.UserModel.objects.get(email=email)
        except self.UserModel.DoesNotExist:
            pass
        except exceptions.MultipleObjectsReturned:
            raise CommandError("Error: That %s is already taken." % email)
        else:
            raise CommandError("Error: That %s is already taken." % email)

        if not username:
            raise CommandError("Error: Blank username aren't allowed.")

        if not password:
            raise CommandError("Error: Blank passwords aren't allowed.")

        if not email:
            raise CommandError("Error: Blank email aren't allowed.")

        user_data = {
            self.UserModel.USERNAME_FIELD: username,
            'email': email,
        }

        self.validate_password(password=password, user_data=user_data, force=force)
        user_data['password'] = password

        if is_superuser:
            self.UserModel.objects.create_superuser(**user_data)
        else:
            self.UserModel.objects.create_user(**user_data)

        if options['verbosity'] >= 1:
            self.stdout.write("{} created successfully.".format(
                'Superuser' if is_superuser else 'User'))
