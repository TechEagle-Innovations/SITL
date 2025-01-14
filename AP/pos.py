import math
import time

import cv2
import cv2.aruco as aruco
import numpy as np


class data:
    x_ang = 0
    y_ang = 0
    distance = 0
    id_to_find = 0
    marker_size = 0


d = data()
file = open('Config.conf', 'r')
p = file.readlines()
for x in p:
    command, value = x.split('=')
    if command == 'ID':
        d.id_to_find = int(value)
    elif command == 'SIZE':
        d.marker_size = int(value)

file.close()
del file
del p

velocity = .5

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters()

##Camera
horizontal_res = 640
vertical_res = 480

horizontal_fov = 62.2 * (math.pi / 180)  # Pi cam V1: 53.5 V2: 62.2
vertical_fov = 48.8 * (math.pi / 180)  # Pi cam V1: 41.41 V2: 48.8

calib_path = "AP/"
cameraMatrix = np.loadtxt(calib_path + 'cameraMatrix.txt', delimiter=',')
cameraDistortion = np.loadtxt(calib_path + 'cameraDistortion.txt', delimiter=',')

# Counters and script triggers
found_count = 0
notfound_count = 0

first_run = 0  # Used to set initial time of function to determine FPS
start_time = 0
end_time = 0
detected = False

'''
returns detected, frame, x_ang, y_ang, distance
'''
def lander(frame):
    global first_run, notfound_count, found_count, start_time
    if first_run == 0:
        print("First run of lander!!")
        first_run = 1
        start_time = time.time()

    frame = cv2.resize(frame, (horizontal_res, vertical_res))
    frame_np = np.array(frame)
    gray_img = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
    ids = ''
    corners, ids, rejected = aruco.detectMarkers(image=gray_img, dictionary=aruco_dict, parameters=parameters)
    try:
        if ids is not None and ids[0] == d.id_to_find:
            y_sum = 0
            x_sum = 0

            x_sum = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
            y_sum = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]

            x_avg = x_sum * .25
            y_avg = y_sum * .25

            d.x_ang = (x_avg - horizontal_res * .5) * (horizontal_fov / horizontal_res)
            d.y_ang = (y_avg - vertical_res * .5) * (vertical_fov / vertical_res)

            aruco.drawDetectedMarkers(frame, corners)
            found_count = found_count + 1
            detected = True
            
            
            # focal_length_x = cameraMatrix[0, 0]
            # apparent_size = corners[0][0][1][0] - corners[0][0][0][0]  # Assuming the marker is rectangular

            # d.distance = (focal_length_x * (d.marker_size/100)) / apparent_size

            # print(f"Distance to ArUco marker {d.id_to_find}: {distance} meters")

        else:
            d.x_ang, d.y_ang = 0, 0
            notfound_count = notfound_count + 1
            detected = False
            
    except Exception as e:
        print('Target likely not found. Error: ' + str(e))
        notfound_count = notfound_count + 1

    return detected, frame, d.x_ang, d.y_ang


class POS:
    def __init__(self, idx, m_size, camera_matrix, camera_Distortion):
        self.show_video = False
        self.id_to_find = idx
        self.marker_size = m_size
        self.velocity = .5

        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = aruco.DetectorParameters()

        ##Camera
        self.horizontal_res = 640
        self.vertical_res = 480

        self.horizontal_fov = 62.2 * (math.pi / 180)  # Pi cam V1: 53.5 V2: 62.2
        self.vertical_fov = 48.8 * (math.pi / 180)  # Pi cam V1: 41.41 V2: 48.8

        self.cameraMatrix = np.loadtxt(camera_matrix, delimiter=',')
        self.cameraDistortion = np.loadtxt(camera_Distortion, delimiter=',')

        # Counters and script triggers
        self.found_count = 0
        self.notfound_count = 0

        self.first_run = 0  # Used to set initial time of function to determine FPS
        self.start_time = 0
        self.end_time = 0
        self.x_ang, self.y_ang = 0, 0

    def lander(self, frame):
        if self.first_run == 0:
            print("First run of lander!!")
            self.first_run = 1
            self.start_time = time.time()

        frame = cv2.resize(frame, (self.horizontal_res, self.vertical_res))
        frame_np = np.array(frame)
        gray_img = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
        ids = ''
        corners, ids, rejected = aruco.detectMarkers(image=gray_img, dictionary=self.aruco_dict,
                                                     parameters=self.parameters)
        try:
            if ids is not None and (ids[0] == 5 or ids[0] == 18):
                ret = aruco.estimatePoseSingleMarkers(corners, self.marker_size, cameraMatrix=self.cameraMatrix,
                                                      distCoeffs=self.cameraDistortion)
                (rvec, tvec) = (ret[0][0, 0, :], ret[1][0, 0, :])
                x = '{:.2f}'.format(tvec[0])
                y = '{:.2f}'.format(tvec[1])
                z = '{:.2f}'.format(tvec[2])

                y_sum = 0
                x_sum = 0

                x_sum = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
                y_sum = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]

                x_avg = x_sum * .25
                y_avg = y_sum * .25

                self.x_ang = (x_avg - self.horizontal_res * .5) * (self.horizontal_fov / self.horizontal_res)
                self.y_ang = (y_avg - self.vertical_res * .5) * (self.vertical_fov / self.vertical_res)
                aruco.drawDetectedMarkers(frame, corners)
                aruco.drawAxis(frame, self.cameraMatrix, self.cameraDistortion, rvec, tvec, 20)
                # print("X CENTER PIXEL: " + str(x_avg) + " Y CENTER PIXEL: " + str(y_avg))
                # print("FOUND COUNT: " + str(found_count) + " NOTFOUND COUNT: " + str(notfound_count))
                # print("MARKER POSITION: x=" + x + " y= " + y + " z=" + z)
                self.found_count += 1
                print("")
            else:
                self.notfound_count += 1
                self.x_ang, self.y_ang = 0, 0
        except Exception as e:
            print('Target likely not found. Error: ' + str(e))
            self.notfound_count += 1

        return frame, self.x_ang, self.y_ang
