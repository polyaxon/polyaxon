import pytest

from db.redis.group_check import GroupChecks
from tests.utils import BaseTest


@pytest.mark.redis_mark
class TestRedisGroupChecks(BaseTest):

    def test_redis_group_checks(self):
        group_checks = GroupChecks(group=1)
        self.assertEqual(group_checks.redis_key_checked, GroupChecks.KEY_CHECKED.format(1))
        self.assertEqual(group_checks.redis_key_delayed, GroupChecks.KEY_DELAYED.format(1))
        self.assertEqual(group_checks.is_checked(), False)
        self.assertEqual(group_checks.is_delayed(), False)

        group_checks.check()
        self.assertEqual(group_checks.is_checked(), True)
        self.assertEqual(group_checks.is_delayed(), False)

        group_checks.clear()
        self.assertEqual(group_checks.is_checked(), False)
        self.assertEqual(group_checks.is_delayed(), False)

        group_checks.delay()
        self.assertEqual(group_checks.is_checked(), True)
        self.assertEqual(group_checks.is_delayed(), True)

        group_checks.clear()
        self.assertEqual(group_checks.is_checked(), False)
        self.assertEqual(group_checks.is_delayed(), False)

        group_checks.check()
        self.assertEqual(group_checks.is_checked(), True)
        self.assertEqual(group_checks.is_delayed(), False)
        group_checks.delay()
        self.assertEqual(group_checks.is_checked(), True)
        self.assertEqual(group_checks.is_delayed(), True)
