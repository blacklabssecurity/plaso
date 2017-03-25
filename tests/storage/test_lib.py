# -*- coding: utf-8 -*-
"""Storage related functions and classes for testing."""

from dfdatetime import filetime as dfdatetime_filetime

from plaso.containers import events
from plaso.containers import time_events
from plaso.containers import windows_events
from plaso.lib import eventdata
from plaso.lib import timelib

from tests import test_lib as shared_test_lib


class StorageTestCase(shared_test_lib.BaseTestCase):
  """The unit test case for a storage object."""

  def _CreateTestEvents(self):
    """Creates events for testing.

    Returns:
      list[EventObject]: events.
    """
    test_events = []
    filetime = dfdatetime_filetime.Filetime()

    event_data = windows_events.WindowsRegistryEventData()
    event_data.key_path = u'MY AutoRun key'
    event_data.parser = u'UNKNOWN'
    event_data.regvalue = {u'Value': u'c:/Temp/evil.exe'}

    filetime.CopyFromString(u'2012-04-20 22:38:46.929596')
    event = time_events.DateTimeValuesEvent(
        filetime, eventdata.EventTimestamp.WRITTEN_TIME)

    self._MergeEventAndEventData(event, event_data)
    test_events.append(event)

    event_data = windows_events.WindowsRegistryEventData()
    event_data.key_path = (
        u'HKEY_CURRENT_USER\\Secret\\EvilEmpire\\Malicious_key')
    event_data.parser = u'UNKNOWN'
    event_data.regvalue = {u'Value': u'send all the exes to the other world'}

    filetime.CopyFromString(u'2012-04-20 23:56:46.929596')
    event = time_events.DateTimeValuesEvent(
        filetime, eventdata.EventTimestamp.WRITTEN_TIME)

    self._MergeEventAndEventData(event, event_data)
    test_events.append(event)

    event_data = windows_events.WindowsRegistryEventData()
    event_data.key_path = u'HKEY_CURRENT_USER\\Windows\\Normal'
    event_data.parser = u'UNKNOWN'
    event_data.regvalue = {u'Value': u'run all the benign stuff'}

    filetime.CopyFromString(u'2012-04-20 16:44:46')
    event = time_events.DateTimeValuesEvent(
        filetime, eventdata.EventTimestamp.WRITTEN_TIME)

    self._MergeEventAndEventData(event, event_data)
    test_events.append(event)

    timestamp = timelib.Timestamp.CopyFromString(u'2009-04-05 12:27:39')

    # TODO: refactor to use event data.
    event = time_events.TimestampEvent(
        timestamp, eventdata.EventTimestamp.WRITTEN_TIME,
        data_type=u'text:entry')
    event.hostname = u'nomachine'
    event.offset = 12
    event.parser = u'UNKNOWN'
    event.text = (
        u'This is a line by someone not reading the log line properly. And '
        u'since this log line exceeds the accepted 80 chars it will be '
        u'shortened.')
    event.username = u'johndoe'
    test_events.append(event)

    return test_events

  def _CreateTestEventTags(self):
    """Creates the event tags for testing.

    Returns:
      A list of event tags (instances of EventTag).
    """
    event_tags = []

    event_tag = events.EventTag()
    event_tag.store_index = 0
    event_tag.store_number = 1
    event_tag.comment = u'My comment'
    event_tags.append(event_tag)

    event_tag = events.EventTag()
    event_tag.store_index = 1
    event_tag.store_number = 1
    event_tag.AddLabel(u'Malware')
    event_tags.append(event_tag)

    event_tag = events.EventTag()
    event_tag.store_number = 1
    event_tag.store_index = 2
    event_tag.comment = u'This is interesting'
    event_tag.AddLabels([u'Malware', u'Benign'])
    event_tags.append(event_tag)

    event_tag = events.EventTag()
    event_tag.store_index = 1
    event_tag.store_number = 1
    event_tag.AddLabel(u'Interesting')
    event_tags.append(event_tag)

    return event_tags

  # TODO: remove after event data refactor.
  def _MergeEventAndEventData(self, event, event_data):
    """Merges the event data with the event.

    args:
      event (EventObject): event.
      event_data (EventData): event_data.
    """
    for attribute_name, attribute_value in event_data.GetAttributes():
      setattr(event, attribute_name, attribute_value)
