"""
Database of Trac tickets

Keep a cache of the seen track tickets. Not all tickets are in the
local database nor are they always up to date, of course.
"""

##############################################################################
#  SageUI: A graphical user interface to Sage, Trac, and Git.
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################



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
        return [ticket for time, ticket in lst[:50]]

