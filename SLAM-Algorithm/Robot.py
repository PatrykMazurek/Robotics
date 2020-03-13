from PiMotor import Motor, Sensor
import Compass
import time, math, keyboard
import numpy as np

# definicja globalnych zmiennych
mL = Motor("MOTOR1", 1)
mR = Motor("MOTOR4", 1)
sen = Sensor("ULTRASONIC", 10)
start_Time = 0.0
end_Time = 0.0
speed = 50
direction = 0.0
realSpeed = 13.5


def DistanceToCheck():
    realDistance = realSpeed * (end_Time - start_Time)
    print("estimated distance traveled: " + str(realDistance))
    return realDistance

# robot control methods
def Forward():
    mL.forward(speed)
    mR.forward(speed)

def Revers():
    mL.reverse(speed)
    mR.reverse(speed)

def TurnLeft(speed_n = 30):
    mL.reverse(speed_n)
    mR.forward(speed_n)

def TurnRight(speed_n = 30):
    mL.forward(speed_n)
    mR.reverse(speed_n)

def StopForward():
    #global move
    mL.stop()
    mR.stop()
    #move = False

def SpecityTheDirection(tab_direction):
    temp_direction = (360.0 - tab_direction[11][0]) + tab_direction[0][0]
    direction = (tab_direction[11][0] + 360 + tab_direction[0][0]) / 2
    for i in range(1, 12):
        if (tab_direction[i][0] - tab_direction[i - 1][0]) > temp_direction:
            temp_direction = (tab_direction[i][0] - tab_direction[i-1][0])
            direction = (tab_direction[i][0] + tab_direction[i][0]) / 2
            print("direction between: " + str(tab_direction[i-1][0]) + " and " + str(tab_direction[i][0]))
    return direction

def TakeMeasurments(x_offset, y_offset):
    # measurements divded into 12 sections every 30 deagress
    sector_range = 12
    angle_value = 30
    sector_executed = float(6)
    list_point = np.zeros((sector_range,2))
    table_range = np.arange(0, 361, sector_range)
    # determining the position in which the robot is located
    start_position = Compass.compass_angle(x_offset, y_offset)
    print("start position: " + str(start_position))
    try:
        for i in range(sector_range):
            min_range = float(i * angle_value)
            max_range = float(min_range + angle_value)
            if min_range < start_position < max_range:
                sector = i
        while True:
            for p in range(sector, sector_range):
                min_range = float(p * angle_value) + sector_executed
                max_range = float(min_range + angle_value) - sector_executed
                work = True
                TurnRight(35)
                while work:
                    if min_range < Compass.compass_angel(x_offset, y_offset) < max_range:
                        StopForward()
                        work = False
                        scan_position = Compass.compass_angle(x_offset, y_offset)
                        distance = sen.distance()
                        if distance > float(450):
                            print("incorrect measurement: " + str(distance))
                            distance = float(0)
                        # [angle, x, y]
                        list_point[p] = [scan_position, distance]
                        print(str(list_point[p]))


            if sector > 0:
                sector_range = sector;
                sector = 0
            else:
                break
        return list_point
    except Exception as e:
        print("error: end of work during measurements")
        print(e)
        return list_point

def MoveToAngle(angle, x_offset, y_offset):
    # placing the robot in the right direction
    sector_range = 12
    angle_value = 30
    sector_executed = 7.5
    start_position = Compass.compass_angle(x_offset, y_offset)
    position = start_position/2
    print("from position: " + str(start_position))
    print("on the direction: " + str(angle))
    min_range = angle - sector_executed
    max_range = angle + sector_executed
    if position < angle <start_position:
        TurnLeft(30)
    else:
        TurnRight(30)

    while True:
        if min_range < Compass.compass_angel(x_offset, y_offset) < max_range:
            StopForward()
            break
    d = sen.distance()
    print("estimated distance to the obstacle " + str(d))

