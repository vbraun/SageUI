

class TracDatabase(object):

    def __init__(self):
        self._data = dict()

    def add_ticket(self, ticket):
        assert isinstance(ticket, TracTicket)
        self._data[ticket.get_number()] = ticket

    def get_ticket(self, ticket_number):
        return self._data[ticket_number]
    
