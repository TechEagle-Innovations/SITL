
from AP.uas import *


print('Connecting...')
drone = Drone('udp::14553')

# @drone.vehicle.on_message('STATUSTEXT')
# def gcs_message_listener(self, name, msg):
#     print(msg)
    
# @drone.vehicle.on_message('AHRS')
# def gcs_message_listener(self, name, msg):
#     print(msg)   
    
@drone.vehicle.on_message('UAV_CRED')
def gcs_message_listener(self, name, msg):
    print(msg)
class flag:
    lock = True
    
f = flag()
    

def main():
    drone.req_credentials(0,"0001MEE0005HEXAC107032024","Hexa@armS3")
    # print('sending request..',1)
    # time.sleep(5)
    #drone.req_credentials(0,"","")
    #drone.preflight_calibration()
    # drone.send_auth_takeoff(1)
    # print('sending request..',0)
    # time.sleep(1)
    while 1:
        # print(f.lock,drone.vehicle.armed)
        # if (f.lock) and (drone.vehicle.armed):
        #     drone.send_auth_takeoff(1)
        #     f.lock = False
        # elif drone.vehicle.armed == False:
        #     f.lock = True
        pass
            
        
            
            
        
    
main()
