import uuid

from datetime import datetime

import pytest
from dateutil.tz import UTC

from event_manager.event import Attribute
from tests.utils import BaseTest


@pytest.mark.events
class TestAttribute(BaseTest):
    def test_name_should_not_be_instance(self):
        with self.assertRaises(AssertionError):
            Attribute(name='instance')

    def test_props(self):
        attr = Attribute(name='test')
        assert attr.name == 'test'
        assert attr.attr_type == str
        assert attr.is_datetime is False
        assert attr.is_uuid is False
        assert attr.is_required is True

    def test_extract(self):
        attr = Attribute(name='test')
        assert attr.extract(value='some value') == 'some value'
        assert attr.extract(value=1) == '1'

        attr = Attribute(name='test', attr_type=int)
        assert attr.extract(value=1) == 1

        attr = Attribute(name='test', is_datetime=True)
        dt = datetime(2000, 12, 12, tzinfo=UTC)
        assert attr.extract(value=dt) == 976579200.0

        attr = Attribute(name='test', is_uuid=True)
        uid = uuid.uuid4()
        assert attr.extract(value=uid) == uid.hex
