import os
import time

import pushover
import requests

from rblchecker.listing import Listing
from rblchecker.probe import Probe

def sendPushMessage(client: pushover.Client, newListings: [Listing], obsoleteListings: [Listing]) -> None:
    message = ""
    if len(newListings) > 0:
        message += "There are new alerts:\n"
        for listing in newListings:
            message += listing.getDescription()
    if len(obsoleteListings):
        message += "The following alerts have been cleared:\n"
        for listing in obsoleteListings:
            message += listing.getDescription()
    client.send_message(message, None, title="RBL Alert")


def Main():
    print("RBLChecker started...")

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

    try:
        client = pushover.Client(pushoverUserKey, api_token=pushoverToken)
    except:
        print("ERROR: Pushover login failed, please provide valid login credentials using the environment variables RBL_PUSHOVER_TOKEN and RBL_PUSHOVER_USER_KEY.")
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
                sendPushMessage(client, newListings, obsoleteListings)

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
