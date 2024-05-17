import os
import adafruit_connection_manager
import wifi
import adafruit_requests
import socketpool
import ssl 
import json
import board
import time 

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)
GREEN = (0, 255, 0)

print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

#  prints MAC address to REPL= 
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pool = socketpool.SocketPool(wifi.radio)
sslContext = ssl.create_default_context() 
requests = adafruit_requests.Session(pool, sslContext)

#todo figure out how specify a certificate....
sslContext.load_verify_locations(cadata="")
requestsInsecure = adafruit_requests.Session(pool, sslContext)

headers = {'Accept': 'application/json','Authorization':'Bearer ' + os.getenv('TOKEN'), 'X-version':'3'}

alerts = requests.get('https://' + os.getenv('COMPANY') + '.logicmonitor.com/santaba/rest/device/groups/' + str(os.getenv('GROUP')) + '/alerts', headers=headers)
#print(alerts.text)
#print(alerts.json()['total'])

while True:
    severity = 0
    
    if alerts.json()['total'] > 0:
        print('total: ' + str(alerts.json()['total']))

    for item in alerts.json()['items']:
        
        print('severity : ' + str(item['severity']))
        print('acked : ' + str(item['acked']))
        print('sdted : ' + str(item['sdted']))
        print('cleared : ' + str(item['cleared']))
        if not item['acked'] and not item['sdted'] and not item['cleared']: 
            if item['severity'] > severity:
                severity = item['severity']

            
    if severity == 0:
        COLOR = GREEN
    if severity == 1:
        COLOR = YELLOW
    if severity == 2:
        COLOR = ORANGE
    if severity == 3:
        COLOR = RED
    # severity 4?


    pixel.fill(COLOR)

    print('...')
    time.sleep(120)
    
