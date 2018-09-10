import base64
import uuid as _uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.crypto import constant_time_compare

from libs.crypto import get_hmac


class EphemeralToken(models.Model):
    KEY_SALT = 'polyaxon.scope.key_salt'

    uuid = models.UUIDField(
        default=_uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    salt = models.UUIDField(
        default=_uuid.uuid4,
        editable=False,
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    num_uses = models.SmallIntegerField(
        blank=True,
        null=True,
        default=1)
    ttl = models.IntegerField(
        null=True,
        blank=True,
        default=60 * 60 * 3)
    scope = ArrayField(
        base_field=models.CharField(max_length=64),
        blank=True,
        null=True)

    @staticmethod
    def clean_timestamp(timestamp):
        """
        Cleans a timestamp to ensure that results are consistent across database
        backends.
        """
        return timestamp.replace(microsecond=0, tzinfo=None)

    @classmethod
    def make_token(cls, ephemeral_token):
        """
        Returns a token to be used x number of times to allow a user account to access
        certain resource.
        """
        created_at = cls.clean_timestamp(ephemeral_token.created_at)
        value = str(created_at) + ephemeral_token.uuid.hex
        if ephemeral_token.scope:
            value += ''.join(ephemeral_token.scope)

        return get_hmac(cls.KEY_SALT + ephemeral_token.salt.hex, value)[::2]

    @classmethod
    def is_timed_out(cls, ephemeral_token):
        """
        Check that if a token is timed out.
        """
        return (timezone.now() - ephemeral_token.created_at).seconds > ephemeral_token.ttl

    @classmethod
    def check_token(cls, ephemeral_token, token):
        """
        Check that a token is correct for a given scope token.
        """
        ephemeral_token.num_uses -= 1

        if ephemeral_token.num_uses < 0:
            ephemeral_token.delete()
            return False

        if cls.is_timed_out(ephemeral_token):
            ephemeral_token.delete()
            return False

        correct_token = cls.make_token(ephemeral_token)

        if ephemeral_token.num_uses <= 0:
            ephemeral_token.delete()
        else:
            ephemeral_token.save()

        return constant_time_compare(correct_token, token)

    @classmethod
    def create_header_token(cls, ephemeral_token):
        token = cls.make_token(ephemeral_token)
        return base64.b64encode(
            '{}XEPH:{}'.format(token, ephemeral_token.uuid.hex).encode('utf-8')).decode("utf-8")

    @staticmethod
    def get_scope(username, model, object_id):
        return ['username:{}'.format(username), '{}:{}'.format(model, object_id)]
