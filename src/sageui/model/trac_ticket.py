"""
A Trac Ticket

EXAMPLES::

    >>> from datetime import datetime
    >>> create_time = datetime.fromtimestamp(1376149000)
    >>> modify_time = datetime.fromtimestamp(1376150000)
    >>> from sageui.model.trac_ticket import TracTicket_class
    >>> t = TracTicket_class(123, create_time, modify_time, {})
    >>> t    # doctest: +ELLIPSIS
    <sageui.model.trac_ticket.TracTicket_class object at 0x...>
    >>> t.get_number()
    123
    >>> t.get_title()
    '+++ no summary +++'
    >>> t.get_ctime()
    datetime.datetime(2013, 8, 10, 16, 36, 40)
    >>> t.get_mtime()
    datetime.datetime(2013, 8, 10, 16, 53, 20)
"""


from datetime import datetime

def make_time(time):
    """
    Convert xmlrpc DateTime objects to datetime.datetime
    """
    if isinstance(time, datetime):
        return time
    return datetime.strptime(time.value, "%Y%m%dT%H:%M:%S")




def TicketChange(changelog_entry):
    time, author, change, data1, data2, data3 = changelog_entry
    # print time, author, change, data1, data2, data3
    if change == 'comment':
        return TicketComment_class(time, author, change, data1, data2, data3)
    return TicketChange_class(time, author, change)


class TicketChange_class(object):
    
    def __init__(self, time, author, change):
        self._time = make_time(time)
        self._author = author
        self._change = change

    def get_ctime(self):
        return self._time

    def get_author(self):
        return self._author
        
    def get_change(self):
        return self._change


class TicketComment_class(TicketChange_class):

    def __init__(self, time, author, change, data1, data2, data3):
        TicketChange_class.__init__(self, time, author, change)
        self._number = data1
        self._comment = data2
        if data3 != 1:
            print 'TicketComment got data3 =', data3

    def get_number(self):
        return self._number

    def get_comment(self):
        return self._comment



def TracTicket(ticket_number, server_proxy):
    ticket_number = int(ticket_number)
    change_log = server_proxy.ticket.changeLog(ticket_number)
    data = server_proxy.ticket.get(ticket_number)
    ticket_changes = [TicketChange(entry) for entry in change_log]
    ticket = TracTicket_class(data[0], data[1], data[2], data[3], ticket_changes)
    ticket.set_download_time(datetime.now())
    return ticket


class TracTicket_class(object):
    
    def __init__(self, number, ctime, mtime, data, change_log=None):
        self._number = number
        self._ctime = make_time(ctime)
        self._mtime = make_time(mtime)
        self._last_viewed = None
        self._download_time = None
        self._data = data
        self._change_log = change_log

    def get_number(self):
        return self._number

    __int__ = get_number

    def get_title(self):
        return self._data.get('summary', '+++ no summary +++')

    def get_ctime(self):
        return self._ctime

    def get_mtime(self):
        return self._mtime

    def get_branch(self):
        branch = self._data.get('branch', '')
        return None if len(branch) == 0 else branch

    def get_dependencies(self):
        deps = self._data.get('dependencies', '')
        return None if len(deps) == 0 else deps

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

    def comment_iter(self):
        for change in self._change_log:
            if isinstance(change, TicketComment_class):
                yield change
        
