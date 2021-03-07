import pushover
import os
import dns.resolver
import re
import time
import requests

RBLS = [
    "all.s5h.net",
    "b.barracudacentral.org",
    "bl.spamcop.net",
    "blacklist.woody.ch",
    "bogons.cymru.com",
    "cbl.abuseat.org",
    "combined.abuse.ch",
    "db.wpbl.info",
    "dnsbl-1.uceprotect.net",
    "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net",
    "dnsbl.dronebl.org",
    "dnsbl.sorbs.net",
    "drone.abuse.ch",
    "duinv.aupads.org",
    "dul.dnsbl.sorbs.net",
    "dyna.spamrats.com",
    "http.dnsbl.sorbs.net",
    "ips.backscatterer.org",
    "ix.dnsbl.manitu.net",
    "korea.services.net",
    "misc.dnsbl.sorbs.net",
    "noptr.spamrats.com",
    "orvedb.aupads.org",
    "pbl.spamhaus.org",
    "proxy.bl.gweep.ca",
    "psbl.surriel.com",
    "relays.bl.gweep.ca",
    "relays.nether.net",
    "sbl.spamhaus.org",
    "singular.ttk.pte.hu",
    "smtp.dnsbl.sorbs.net",
    "socks.dnsbl.sorbs.net",
    "spam.abuse.ch",
    "spam.dnsbl.anonmails.de",
    "spam.dnsbl.sorbs.net",
    "spam.spamrats.com",
    "spambot.bls.digibase.ca",
    "spamrbl.imp.ch",
    "spamsources.fabel.dk",
    "ubl.lashback.com",
    "ubl.unsubscore.com",
    "virus.rbl.jp",
    "web.dnsbl.sorbs.net",
    "wormrbl.imp.ch",
    "xbl.spamhaus.org",
    "z.mailspike.net",
    "zen.spamhaus.org",
    "zombie.dnsbl.sorbs.net"
]


def Main():
    print("RBLWatch started...")

    # Get enviornment variables
    hosts = os.environ.get('RBL_HOSTS', "")  # Comma separated list
    pushoverToken = os.environ.get('RBL_PUSHOVER_TOKEN', "")
    pushoverUserKey = os.environ.get('RBL_PUSHOVER_USER_KEY', "")
    interval = os.environ.get('RBL_INTERVAL', 60)  # Given in minutes
    # May be used to report execution to a healthchecks server
    healthcheckUrl = os.environ.get('RBL_HEALTHCHECK_URL', "")

    # Make sure that all required variables are provided
    if (hosts == "" or pushoverToken == "" or pushoverUserKey == ""):
        print("Please supply RBL_HOSTS, RBL_PUSHOVER_TOKEN and RBL_PUSHOVER_USER_KEY as environment variables")
        exit(1)

    client = pushover.Client(pushoverUserKey, api_token=pushoverToken)

    ip_Pattern = re.compile(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")

    while True:
        for host in hosts.split(","):
            print("Checking blacklists for " + host)

            # Resolve DNS name, if required
            isIpAddress = ip_Pattern.match(host)
            if isIpAddress:
                ip = host
            else:
                ipReply = dns.resolver.resolve(host, 'A')
                ip = ipReply[0].address

            ipReverse = ip.split(".")[3] + "." + ip.split(".")[2] + "." + ip.split(".")[1] + "." + ip.split(".")[0]

            for rbl in RBLS:
                try:
                    # Octets of IP reversed + rbl name
                    rblReply = dns.resolver.resolve(ipReverse + "." + rbl, 'A')
                    print("Listed here: " + rbl + ", Reply was: " + rblReply[0].address)
                    message = "Server " + host + " is listed on this RBL: " + rbl + "\n"
                    message += "The DNS reply was: " + rblReply[0].address + "\n"
                    # Reason for blocking might be given in TXT record
                    try:
                        rblReply = dns.resolver.resolve(ipReverse + "." + rbl, 'TXT')
                        for reply in rblReply:
                            print("Reason given for listing:")
                            print(reply)
                            message += "Reason: " + str(reply)
                    except:
                        pass
                    # Send pushover message
                    client.send_message(message, title="Server found on RBL")
                except dns.resolver.NXDOMAIN:
                    # print("not listed here: " + rbl)
                    pass
                except dns.resolver.NoAnswer:
                    # print("not listed here: " + rbl)
                    pass
                except dns.resolver.Timeout:
                    # print("Timeout from " + rbl)
                    pass
                except:
                    # print("Something went wrong here: " + rbl)
                    pass

        # Checking done. Report health to healthcheck server
        if(healthcheckUrl != ""):
            try:
                requests.get(healthcheckUrl, timeout = 10)
            except:
                print("Healthcheck server not reachable")

        # Go to sleep
        print("Sleeping for " + str(interval) + " Minutes")
        time.sleep(int(interval) * 60)


if __name__ == '__main__':
    Main()
