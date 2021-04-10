import os
import time

import apprise
import requests

from rblchecker.listing import Listing
from rblchecker.probe import Probe

def notify(appriseObject: apprise.Apprise, newListings: [Listing], obsoleteListings: [Listing]) -> None:
    message = ""
    if len(newListings) > 0:
        message += "There are new alerts:\n"
        for listing in newListings:
            message += listing.getDescription()
    if len(obsoleteListings):
        message += "The following alerts have been cleared:\n"
        for listing in obsoleteListings:
            message += listing.getDescription()
    appriseObject.notify(body = message, title = "RBL Alert")


def Main():
    print("RBLChecker started...")

    # Get environment variables
    hosts = os.environ.get('RBL_HOSTS', "")  # Comma separated list
    appriseUrl = os.environ.get('RBL_APPRISE_URL', "")
    interval = os.environ.get('RBL_INTERVAL', 60)  # Given in minutes
    # May be used to report execution to a healthchecks server
    healthcheckUrl = os.environ.get('RBL_HEALTHCHECK_URL', "")

    # Make sure that all required variables are provided
    if (hosts == "" or appriseUrl == ""):
        print("Please supply RBL_HOSTS and RBL_APPRISE_URL as environment variables")
        exit(1)

    try:
        appriseObject = apprise.Apprise()
        appriseObject.add(appriseUrl)
    except:
        print("ERROR: Apprise initialization failed. Please double-check your configuration.")
        print("Exiting...")
        exit(1)

    probes = []
    for host in hosts.split(","):
        probes.append(Probe(host))

    while True:
        for probe in probes:
            print("Checking blacklists for " + probe.host)
            (newListings, obsoleteListings) = probe.check()

            if len(newListings) > 0 or len(obsoleteListings) > 0:
                notify(appriseObject, newListings, obsoleteListings)

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
