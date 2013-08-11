"""
Database of Trac tickets

Keep a cache of the seen track tickets. Not all tickets are in the
local database nor are they always up to date, of course.
"""

import cPickle
import os

from trac_ticket import TracTicket, TracTicket_class



class TracDatabase(object):

    def __init__(self):
        self._data = dict()

    def save(self, directory_name):
        filename = os.path.join(directory_name,
        'trac_database.pickle') 
        try:
            with open(filename, 'wb') as pickle:
                cPickle.dump(self._data, pickle)
            return True
        except (IOError, OSError, cPickle.UnpicklingError, TypeError):
            self._data = dict()
            return False
        
    def load(self, directory_name):
        filename = os.path.join(directory_name, 'trac_database.pickle')
        try:
            with open(filename, 'rb') as pickle:
                self._data = cPickle.load(pickle)
            return True
        except (IOError, OSError, cPickle.UnpicklingError, TypeError):
            self._data = dict()
            return False

    def add(self, ticket):
        assert isinstance(ticket, TracTicket_class)
        number = ticket.get_number()
        current = self._data.get(number, None)
        if current is not None:
            ticket.set_last_viewed_time(current.get_last_viewed_time())
        self._data[number] = ticket

    def get(self, ticket_number):
        return self._data[ticket_number]
    
    def recent_tickets(self, limit=50):
        lst = [(ticket.get_last_viewed_time(), ticket) 
               for ticket in self._data.values()]
        lst.sort(reverse=True)
        return tuple(ticket for time, ticket in lst[:50])

