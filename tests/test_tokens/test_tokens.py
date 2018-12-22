from datetime import timedelta

import pytest

from django.conf import settings
from django.utils import timezone

from db.models.tokens import Token
from tests.utils import BaseTest


@pytest.mark.api_tokens_mark
class TokenTest(BaseTest):
    def test_is_expired(self):
        token = Token()
        self.assertEqual(token.is_expired, False)

        token = Token(started_at=timezone.now() + timedelta(days=1))
        self.assertEqual(token.is_expired, False)

        token = Token(started_at=timezone.now() - timedelta(days=settings.TTL_TOKEN + 10))
        self.assertEqual(token.is_expired, True)

    def test_get_scopes(self):
        token = Token()
        assert token.scopes == []

        token = Token(scopes=['project:read', 'project:write'])
        assert token.scopes == ['project:read', 'project:write']
