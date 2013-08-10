"""
Interface to the Sage Trac server

Uses XML-RPC to talk to the trac server.

EXAMPLES::


"""

from trac_ticket import TracTicket
from trac_database import TracDatabase


class TracServer(object):

    def __init__(self, server, anonymous_location):
        self.server = server
        self.database = TracDatabase()
        self.anonymous_proxy = self._create_anonymous_server_proxy(server, anonymous_location)
        self.authenticated_proxy = None

    def _create_anonymous_server_proxy(self, url_server, url_location):
        import urlparse
        url = urlparse.urljoin(url_server, url_location)
        from digest_transport import DigestTransport
        transport = DigestTransport()
        from xmlrpclib import ServerProxy
        return ServerProxy(url, transport=transport)

    def load(self, ticket_number):
        data = self.anonymous_proxy.ticket.get(ticket_number)
        title = data[3].get('summary', '+++ No Summary +++')
        ticket = TracTicket(data[0], title, data[1], data[2], data[3])
        self.database.add(ticket)
        return ticket

    def get(self, ticket_number):
        return self.database.get(ticket_number)
