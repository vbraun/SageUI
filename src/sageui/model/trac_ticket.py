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
        self._download_time = None
        self._data = data

    def get_number(self):
        return self._number

    __int__ = get_number

    def get_title(self):
        return self._title

    def get_ctime(self):
        return self._ctime

    def get_mtime(self):
        return self._mtime

    def get_branch(self):
        branch = self._data.get('branch', '')
        return None if len(branch) == 0 else branch

    def _pretty_time(self, time):
        """
        Return a pretty string like 'an hour ago', 'Yesterday', '3 months
        ago', 'just now', etc
        """
        now = datetime.now()
        diff = now - time
        second_diff = diff.seconds
        day_diff = diff.days
        if day_diff < 0:
            return 'from future?'
        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return  "a minute ago"
            if second_diff < 3600:
                return str( second_diff / 60 ) + " minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str( second_diff / 3600 ) + " hours ago"
        if day_diff == 1:
            return "yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff/7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff/30) + " months ago"
        return str(day_diff/365) + " years ago"

    def set_last_viewed_time(self, time):
        self._last_viewed = time

    def get_last_viewed_time(self):
        t = self._last_viewed
        if t is None:
            return datetime.min
        else:
            return t

    def get_pretty_last_viewed_time(self):
        return self._pretty_time(self.get_last_viewed_time())
    
    def set_download_time(self, time):
        self._download_time = time

    def get_download_time(self):
        t = self._download_time
        if t is None:
            return datetime.min
        else:
            return t

    def get_pretty_download_time(self):
        return self._pretty_time(self.get_download_time())
    
    def get_description(self):
        default = '+++ no description +++'
        return self._data.get('description', default)

