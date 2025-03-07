import dns.resolver
from ipaddress import ip_address
from rblchecker.listing import Listing

class Probe(object):
 
    def __init__(self, host: str, dqsKey: str):
        self._hostToCheck = host
        self._dqsKey = dqsKey
        self._ipsToCheck = self._resolveToIPs()
        self._listings = []
        self.initializeRBLs()
    
    @property
    def host(self) -> str:
        return self._hostToCheck

    def check(self) -> ([Listing], [Listing]):
        """Checks weather the given host is listed on any dns blacklist, returns an array of new listings, and one of obsolete ones"""

        currentListings = []

        for ip in self._ipsToCheck:
            for bl in self.RBLs:
                try:
                    reply = dns.resolver.resolve(self._generateLookupUrl(ip,bl), 'A')
                    # If this point is reached, the IP address was listed
                    # Try to find out the reason by getting the corresponding TXT record
                    listing = Listing(self._hostToCheck, ip, bl)
                    try:
                        reply = dns.resolver.resolve(self._generateLookupUrl(ip,bl), 'TXT')
                        for record in reply:
                            listing.addReason(str(record)) 
                    except:
                        pass

                    currentListings.append(listing)

                except dns.resolver.NXDOMAIN:
                    # Not listed
                    pass
                except dns.resolver.NoAnswer:
                     # Not listed
                    pass
                except dns.resolver.NoNameservers:
                    print("All nameservers dailed to answer the query, RBL is probably misconfigured: " + bl)
                except dns.resolver.Timeout:
                    # No DNS reply received in time
                    print("Timeout from " + bl)
        
        # Process the observed listings
        # Newly observed listings
        newListings = list(set(currentListings) - set(self._listings))
        # Listings that have been removed
        obsoleteListings = list(set(self._listings) - set(currentListings))

        self._listings = currentListings

        return (newListings, obsoleteListings)

    def _isValidIPAddress(self, IP: str) -> bool: 
        try: 
            ip_address(IP)
            return True
        except ValueError: 
            return False

    
    def _resolveToIPs(self) -> [str]:
        """Fetches all A and AAAA DNS records for the given hostname and returns them as an array"""

        if self._isValidIPAddress(self._hostToCheck):
            return [self._hostToCheck]
        else:
            # Assume it is a hostname otherwise, resolve it
            try:
                replyv4 = dns.resolver.resolve(self._hostToCheck, 'A')
            except:
                replyv4 = []
            try:
                replyv6 = dns.resolver.resolve(self._hostToCheck, 'AAAA')
            except:
                replyv6 = []
            ipv4s = list(map(lambda reply: reply.address, replyv4))
            ipv6s = list(map(lambda reply: reply.address, replyv6))
            return ipv4s + ipv6s

    def _generateLookupUrl(self, ip: str, dnsbl: str) -> str:
        """Given an IP address and a dnsbl, generates a valid lookup address (RFC5782)"""

        return ".".join(ip_address(ip).reverse_pointer.split('.')[0:-2]) + '.' + dnsbl
    def initializeRBLs(self):
        self.RBLs = [
            'zombie.dnsbl.sorbs.net',
            'bl.spamcop.net',
            'dsn.rfc-ignorant.org',
            'multi.surbl.org',
            'blackholes.five-ten-sg.com',
            'sorbs.dnsbl.net.au',
            'dnsbl.sorbs.net',
            'zen.spamhaus.org' if self._dqsKey == "" else "".join([self._dqsKey, ".zen.dq.spamhaus.net"]),
            'db.wpbl.info',
            'rmst.dnsbl.net.au',
            'dnsbl.kempt.net',
            'blacklist.woody.ch',
            'psbl.surriel.com',
            'virbl.bit.nl',
            'virus.rbl.jp',
            'wormrbl.imp.ch',
            'spamrbl.imp.ch',
            'rbl.interserver.net',
            'spamlist.or.kr',
            'dyna.spamrats.com',
            'dnsbl.abuse.ch',
            'dnsbl.inps.de',
            'dnsbl.dronebl.org',
            'bl.deadbeef.com',
            'ricn.dnsbl.net.au',
            'forbidden.icm.edu.pl',
            'probes.dnsbl.net.au',
            'ubl.unsubscore.com',
            'b.barracudacentral.org',
            'ksi.dnsbl.net.au',
            'uribl.swinog.ch',
            'bsb.spamlookup.net',
            'dob.sibl.support-intelligence.net',
            'url.rbl.jp',
            'dyndns.rbl.jp',
            'bogons.cymru.com',
            'relays.mail-abuse.org',
            'omrs.dnsbl.net.au',
            'osrs.dnsbl.net.au',
            'orvedb.aupads.org',
            'relays.nether.net',
            'relays.bl.gweep.ca',
            'smtp.dnsbl.sorbs.net',
            'relays.bl.kundenserver.de',
            'dialups.mail-abuse.org',
            'rdts.dnsbl.net.au',
            'spam.dnsbl.sorbs.net',
            'duinv.aupads.org',
            'dynablock.sorbs.net',
            'dynip.rothen.com',
            'short.rbl.jp',
            'korea.services.net',
            'mail.people.it',
            'blacklist.sci.kun.nl',
            'all.spamblock.unit.liu.se'
        ]