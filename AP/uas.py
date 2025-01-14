from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import math as m
import numpy as np
import time


class Drone:
    def __init__(self, connection_string):
        self.vehicle = connect(connection_string)

    def arm_and_takeoff(self, altitude):
        while not self.vehicle.is_armable:
            print("waiting to be armable")
            time.sleep(1)

        print("Arming motors")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            time.sleep(1)

        print("Taking Off")
        self.vehicle.simple_takeoff(altitude)

        while True:
            v_alt = self.vehicle.location.global_relative_frame.alt
            print(">> Altitude = %.1f m" % v_alt)
            if v_alt >= altitude - 1.0:
                print("Target altitude reached")
                break
            time.sleep(1)

    def send_land_message(self, x, y, distance, time_usec=0, target_num=0):

        msg = self.vehicle.message_factory.landing_target_encode(
            time_usec,  # time target data was processed, as close to sensor capture as possible
            target_num,  # target num, not used
            mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame, not used
            x,  # X-axis angular offset, in radians, for hexa (-x) 
            y,  # Y-axis angular offset, in radians, for hexa (-y) 
            distance,  # distance, in meters
            0,  # Target x-axis size, in radians
            0,  # Target y-axis size, in radians
            0,  # x	float	X Position of the landing target on MAV_FRAME
            0,  # y	float	Y Position of the landing target on MAV_FRAME
            0,  # z	float	Z Position of the landing target on MAV_FRAME
            (1, 0, 0, 0),
            # q	float[4]	Quaternion of landing target orientation (w, x, y, z order, zero-rotation is 1, 0, 0, 0)
            2,  # type of landing target: 2 = Fiducial marker
            1,  # position_valid boolean
        )
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()

    def send_msg_to_gcs(self, text_to_be_sent):
        # MAV_SEVERITY: 0=EMERGENCY 1=ALERT 2=CRITICAL 3=ERROR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG, 8=ENUM_END
        # Defined here: https://mavlink.io/en/messages/common.html#MAV_SEVERITY
        # MAV_SEVERITY = 3 will let the message be displayed on Mission Planner HUD, but 6 is ok for QGroundControl
        if self.vehicle is not None:
            text_msg = 'OA: ' + text_to_be_sent
            status_msg = self.vehicle.message_factory.statustext_encode(
                6,  # MAV_SEVERITY
                text_msg.encode()  # max size is char[50]
            )
            self.vehicle.send_mavlink(status_msg)
            self.vehicle.flush()
            print("INFO: " + text_to_be_sent)
        else:
            print("INFO: Vehicle not connected. Cannot send text message to Ground Control Station (GCS)")

    def send_auth_takeoff(self, status):
        msg = self.vehicle.message_factory.auth_takeoff_encode(status = status)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def send_ipls_sensor_status(self, status):
        msg = self.vehicle.message_factory.land_sensor_status_encode(sensor_status = status)
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def req_credentials(self, status, uas_id, password):
        msg = self.vehicle.message_factory.req_uav_cred_encode(
            status = status, 
            uav_id = uas_id.encode('utf-8'),
            password=password.encode('utf-8')
        )
        
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def req_flight_status(self, P1):
        msg = self.vehicle.message_factory.req_flt_status_encode(
            P1 = P1, 
        )
        
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def req_clearsky_info(self, P1):
        msg = self.vehicle.message_factory.req_clearsky_encode(
            request = P1, 
        )
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
        
    def preflight_calibration(self):
        msg = self.vehicle.message_factory.command_long_encode(
            0, 
            0,  # target_system, target_component
            mavutil.mavlink.MAV_CMD_PREFLIGHT_CALIBRATION,  # command
            0,  # confirmation
            0,  # param 1, 1: gyro calibration, 3: gyro temperature calibration
            0,  # param 2, 1: magnetometer calibration
            1,  # param 3, 1: ground pressure calibration
            0,  # param 4, 1: radio RC calibration, 2: RC trim calibration
            0,  # param 5, 1: accelerometer calibration, 2: board level calibration, 3: accelerometer temperature calibration, 4: simple accelerometer calibration
            0,  # param 6, 2: airspeed calibration
            0,  # param 7, 1: ESC calibration, 3: barometer temperature calibration
        )
        self.vehicle.send_mavlink(msg)
        self.vehicle.flush()
    

