#!/usr/local/bin/python3
import logging
import os
import time

import requests

# park and ride
chargerId = '2104'
# the ivanhoe
# chargerId = '608'
url = 'https://myaccount.esbecars.com/stationFacade/findStationById?stationId=' + chargerId

hours = 10
minutes = 60
timesToTry = hours * minutes

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def get_sockets():
    response = requests.get(url)
    # print(json.dumps(response.json(), indent=2))
    return response.json()['data']['stationSockets']


def determine_availability(sockets):
    available = False
    for stationSocket in sockets:
        name = stationSocket['name']
        socket_status = stationSocket['socketStatusId']

        if 'chargeTransactionStartTime' in stationSocket:
            start_time = stationSocket['chargeTransactionStartTime']
            minutes_since_start = int((time.time() - start_time / 1000) / 60)
            logging.info(
                'Charger: {} is {}. Session started {} minutes ago.'.format(name, socket_status, minutes_since_start))
        else:
            logging.info('Charger: {} is {}.'.format(name, socket_status))

        if socket_status == 'AVAILABLE':
            available = True

    return available


def notify(available):
    if available:
        logging.info('Charger ' + chargerId + ' is available')
        macos_notify("Charger Available", 'Charger ' + chargerId + ' is available')
    else:
        logging.info('Charger is not available')
        # macos_notify("Charger Busy", 'Charger ' + chargerId + ' is busy')


def macos_notify(title, text):
    # os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))
    # os.system("""osascript -e 'tell app "Finder" to display dialog "Hello World"'""".format(text, title))
    os.system("""osascript -e 'tell app "System Events" to display dialog "{}" with title "{}"'""".format(text, title))


def do_work():
    for i in range(timesToTry):
        sockets = get_sockets()
        available = determine_availability(sockets)
        notify(available)
        time.sleep(60)


do_work()
