import http.server
import socketserver
import os
from gpiozero import LED
import time
PORT = 9001

"""Part of the 3 servo reciever code cinematic universe"""

# bits: Fill Servo, NOX Servo, ETH/MAIN Servo
# 1 = OPEN, 0 = Close, X = Previous State/Doesnt Matter
# Concept Behind This Code:
# State      | DPF | IREC
# ------------------------------------------
# Close      | X00 | 0X0
# Fire       | 011 | 0X1
# Abort      | 001 | 0X1
# Fill       | 100 | 1X0
# Close Fill | 000 | 0X0

# fire - 17
# armFire - 27
# fill - 22
# externalETH - 23
# externalNOX - 24
# externalFIL - 25


fire = LED(17)
armFire = LED(27)
fill = LED(22)
externalETH = LED(23)
externalNOX = LED(24)
externalFIL = LED(25)


def set_servos(State):
    if (State == 'close'):  # all off
        externalETH.off()
        externalNOX.off()
        externalFIL.off()
    elif (State == 'fire'):
        externalETH.on()
        externalNOX.on()
        externalFIL.off()
    elif (State == 'abort'):
        externalETH.on()
        externalNOX.off()
        externalFIL.off()
    elif (State == 'fill'):
        externalETH.off()
        externalNOX.off()
        externalFIL.on()
    elif (State == 'close_fill'):
        externalETH.off()
        externalNOX.off()
        externalFIL.off()
    else:
        print("States are not properly")


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        #        if(self.path == "/v"):
        # print("Vent")

        #        elif(self.path == "/vc"):
        # print("Vent close")

        if (self.path == "/f"):
            # print("Fill")
            set_servos('fill')

        elif (self.path == "/fc"):
           # print("Fill close")
            set_servos('close_fill')

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
