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
# fill - 22
# externalETH - 23
# externalNOX - 24
# externalFIL - 25


fire = LED(17)
armFire = LED(27)
externalETH = LED(23)
externalNOX = LED(24)
externalFIL = LED(25)
externalVEN = LED(26)


def set_servos(State):
    if (State == 'close'):  # all off
        externalETH.off()
        externalNOX.off()
    elif (State == 'fire'):
        externalETH.on()
        externalNOX.on()
        externalFIL.off()
        externalVEN.off()
    elif (State == 'abort'):
        externalETH.on()
        externalNOX.off()
        externalFIL.off()
        externalVEN.off()
    elif (State == 'fill'):
        externalETH.off()
        externalNOX.off()
        externalFIL.on()
        externalVEN.off()
    elif (State == 'vent'):
        externalETH.off()
        externalNOX.off()
        externalFIL.off()
        externalVEN.off()
    elif (State == 'close_vent'):
        externalVEN.off()
    elif (State == 'close_fill'):
        externalFIL.off()

    else:
        print("States are not properly")


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if (self.path == "/v"):
            # print("Vent")
            set_servos('vent')
        elif (self.path == "/vc"):
            # print("Vent close")
            set_servos('close')
        elif (self.path == "/f"):
            # print("Fill")
            set_servos('fill')

        elif (self.path == "/fc"):
           # print("Fill close")
            set_servos('close')

        elif (self.path == "/m"):
           # print("Arm E-Match")
            armFire.on()

        elif (self.path == "/mc"):
            # print("Disarm E-Match")
            armFire.off()

        elif (self.path == "/e"):
           # print("Fire!!")
            fire.on()
            time.sleep(0.2)
            set_servos('fire')
            time.sleep(0.1)
            fire.off()

        elif (self.path == "/q"):
            # print("Close valves")
            set_servos('close')

        elif (self.path == "/a"):
            # print("Abort")
            set_servos('abort')


        # print(self.path)
        # print(self.headers)
Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # print("Http Server Serving at port", PORT)
    httpd.serve_forever()
