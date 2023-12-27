
from AP.uas import *

print('Connecting...')
drone = Drone('udp::14553')


def main():
    drone.send_auth_takeoff(12)
   
main()
