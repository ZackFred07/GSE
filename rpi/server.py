import http.server
import socketserver
import os
from gpiozero import LED
import time
PORT = 9001

"""Part of the 3 servo reciever code cinematic universe"""

# Pins based on bits
# VEN - 0
# FIL - 1
# NOX - 2
# ETH - 3
# 1 = OPEN, 0 = Close, X = Previous State/Doesnt Matter
# Concept Behind This Code:
# State      | DPF | IREC
# ------------------------------------------
# Close ALL  | 0000 | 00X0
# Fire       | 0011 | 00X1
# Abort      | 0010 | 00X0
# Fill       | 0100 | 01X0
# Vent       | 1000 | 10X0
# Close Vent | 0XXX | 0XXX
# Close Fill | X0XX | X0XX
# fire - 17
# armFire - 27
# externalETH - 23
# externalNOX - 24
# externalFIL - 25
# externalVEN - 26

fire = LED(17)
armFire = LED(27)
# fill = LED(22)
externalETH = LED(23)
externalNOX = LED(24)
externalFIL = LED(25)
externalVEN = LED(21)
externalIDK = LED(26)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if (self.path == "/v"):
            print("Vent")
            externalVEN.on()
        elif (self.path == "/vc"):
            print("Vent close")
            externalVEN.off()
        elif (self.path == "/f"):
            print("Fill")
            externalFIL.on()
        elif (self.path == "/fc"):
            print("Fill close")
            externalFIL.off()
        elif (self.path == "/m"):
            print("Arm E-Match")
            armFire.on()
            armFire.off()
        elif (self.path == "/e"):
            print("Fire!!")
            fire.on()
            time.sleep(0.2)
            externalETH.on()
            externalNOX.on()
            time.sleep(0.1)
            fire.off()
        elif (self.path == "/q"):
            print("Close valves")
            externalETH.off()
            externalNOX.off()
        elif (self.path == "/a"):
            print("Abort")
            externalETH.off()
            externalNOX.on()

        # print(self.path)
        # print(self.headers)
Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # print("Http Server Serving at port", PORT)
    httpd.serve_forever()
