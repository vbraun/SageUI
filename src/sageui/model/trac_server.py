"""
Interface to the Sage Trac server

Uses XML-RPC to talk to the trac server.

EXAMPLES::


"""
from datetime import datetime

from trac_ticket import TracTicket
from trac_database import TracDatabase


class TracServer(object):

    def __init__(self, server, anonymous_location):
        self.server = server
        self.database = TracDatabase()
        self.anonymous_proxy = self._create_anonymous_server_proxy(server, anonymous_location)
        self.authenticated_proxy = None
        self._current_ticket_number = None

    def _create_anonymous_server_proxy(self, url_server, url_location):
        import urlparse
        url = urlparse.urljoin(url_server, url_location)
        from digest_transport import DigestTransport
        transport = DigestTransport()
        from xmlrpclib import ServerProxy
        return ServerProxy(url, transport=transport)

    def load(self, ticket_number):
        ticket_number = int(ticket_number)
        data = self.anonymous_proxy.ticket.get(ticket_number)
        title = data[3].get('summary', '+++ No Summary +++')
        ticket = TracTicket(data[0], title, data[1], data[2], data[3])
        ticket.set_download_time(datetime.now())
        self.database.add(ticket)
        return ticket

    def get(self, ticket_number):
        ticket_number = int(ticket_number)
        return self.database.get(ticket_number)

    def set_current_ticket(self, ticket_number):
        ticket_number = int(ticket_number)
        self._current_ticket_number = ticket_number
        try:
            self.get(ticket_number).set_last_viewed_time(datetime.now())
        except KeyError:
            pass

    def get_current_ticket(self):
        """
        Return the current ticket.

        OUTPUT:

        A ticket, always the same until :meth:`set_current_ticket` 
        is used to change it. May be ``None`` if no current ticket
        has been set yet.
        """
        curr = self._current_ticket_number
        if curr is None:
            return None
        try:
            return self.get(curr)
        except KeyError:
            return self.load(curr)
