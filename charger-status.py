import requests
import os


# park and ride
chargerId = '2104'
# the ivanhoe
# chargerId = '608'

url = 'https://myaccount.esbecars.com/stationFacade/findStationById?stationId=' + chargerId
response = requests.get(url)
stationSockets = response.json()['data']['stationSockets']

available = False

for stationSocket in stationSockets:
    print(stationSocket['socketStatusId'])
    socketStatus = stationSocket['socketStatusId']
    if socketStatus == 'AVAILABLE':
        available = True


def notify(title, text):
    # os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))
    # os.system("""osascript -e 'tell app "Finder" to display dialog "Hello World"'""".format(text, title))
    os.system("""osascript -e 'tell app "System Events" to display dialog "{}" with title "{}"'""".format(text, title))


if available:
    print('Charger ' + chargerId + ' is available')
    notify("Charger Available", 'Charger ' + chargerId + ' is available')
else:
    print('Charger is not available')

