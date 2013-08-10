"""
A Trac Ticket

EXAMPLES::

    >>> from sageui.model.trac_ticket import TracTicket
    >>> t = TracTicket(123, 'ticket title', 1376149000, 1376150000)
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
    
    def __init__(self, number, title, modified_time_unix, last_viewed_unix):
        self._number = number
        self._title = title
        self._modified_time_unix = modified_time_unix
        self._last_viewed_unix = last_viewed_unix

    def get_number(self):
        return self._number

    def get_title(self):
        return self._title

    def get_modified_time(self):
        return datetime.fromtimestamp(self._modified_time_unix)

    def get_last_viewed(self):
        return datetime.fromtimestamp(self._last_viewed_unix)
