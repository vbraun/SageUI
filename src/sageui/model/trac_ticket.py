"""
A Trac Ticket

EXAMPLES::

    >>> from datetime import datetime
    >>> create_time = datetime.fromtimestamp(1376149000)
    >>> modify_time = datetime.fromtimestamp(1376150000)
    >>> from sageui.model.trac_ticket import TracTicket
    >>> t = TracTicket(123, 'ticket title', create_time, modify_time, {})
    >>> t    # doctest: +ELLIPSIS
    <sageui.model.trac_ticket.TracTicket object at 0x...>
    >>> t.get_number()
    123
     t.get_title()
    'ticket title'
    >>> t.get_modified_time()
    datetime.datetime(2013, 8, 10, 16, 36, 40)
    >>> t.get_last_viewed()
    datetime.datetime(2013, 8, 10, 16, 53, 20)
"""


from datetime import datetime


class TracTicket(object):
    
    def __init__(self, number, title, ctime, mtime, data):
        self._number = number
        self._title = title
        self._ctime = ctime
        self._mtime = mtime
        self._last_viewed = None
        self._data = data

    def get_number(self):
        return self._number

    def get_title(self):
        return self._title

    def get_ctime(self):
        return self._ctime

    def get_mtime(self):
        return self._mtime

    def set_last_viewed_time(self, time):
        self._last_viewed = time

    def get_last_viewed_time(self):
        return self._last_viewed
