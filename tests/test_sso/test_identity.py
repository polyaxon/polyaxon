import pytest

from factories.factory_users import UserFactory
from sso.wizard import IdentityWizard
from tests.utils import BaseTest


@pytest.mark.libs_mark
class TestIdentityWizard(BaseTest):
    def test_validate_username(self):
        user = UserFactory(username='sdf1')
        self.assertEqual(IdentityWizard.validate_username('sdf sdf'), 'sdf-sdf')
        self.assertEqual(IdentityWizard.validate_username('sdf.sdf'), 'sdf-sdf')
        self.assertEqual(IdentityWizard.validate_username('sdf'), 'sdf')
        self.assertNotEqual(IdentityWizard.validate_username(user.username), user.username)
