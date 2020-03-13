import threading, time, math
import keyboard
from PiMotor import Motor, Sensor
import numpy as np, cv2
import Compass, Robot

#zmienne globalne
timeWork = 0
speed = 45
direction = ""
position_mmaping = {}
move = False
finish = False
work = False
callibration = False


if __name__ == '__main__':
    try:

        measursment_list = []
        with open("compass-offset.csv", "r") as f:
            temp = f.readline().split(';')
            x_csv_offset = float(temp[0])
            y_csv_offset = float(temp[1])
        i = 0
        # first measurement and determination of the robot's position
        position = Robot.TakeMeasurments(x_csv_offset, y_csv_offset)

        position_mmaping[i] = position
        old_x = 0.0
        old_y = 0.0
        measursment_list.append([old_x,old_y, 0.0, 0.0])

        roud = Robot.SpecityTheDirection(position_mmaping[i])
        i = i + 1
        print("angle: " + str(roud))
        Robot.MoveToAngle(roud, x_csv_offset, y_csv_offset)

        work = True
        while work:
            start_dystans = Robot.sen.distance()
            Robot.start_Time = time.time()
            Robot.Forward()
            while True:
                if Robot.sen.distance() < 50:
                    Robot.StopForward()
                    Robot.end_Time = time.time()
                    print("start new measurement")
                    time.sleep(0.5)
                    # determining the distance traveled
                    print("new positons: ")
                    new_posittion = Compass.compass_angle(x_csv_offset, y_csv_offset)
                    #print("angle: " + str(roud) )
                    #print("angle after stopping: " + str(new_posittion))
                    #print("determining the distance:")
                    real_roud = Robot.DistanceToCheck()
                    # determining the new postion
                    new_x = real_roud * math.cos(np.radians(new_posittion)) + old_x
                    new_y = real_roud * math.sin(np.radians(new_posittion)) + old_y
                    print("position x: " + str(new_x) + " y " + str(new_y))
                    # making distance measurements
                    
                    position = Robot.TakeMeasurments(x_csv_offset, y_csv_offset)
                    position_mmaping[i] = position
                    measursment_list.append([new_x, new_y, real_roud, new_posittion])
                    old_x = new_x
                    old_y = new_y
                    i = i + 1
                    # definig a new path
                    roud = Robot.SpecityTheDirection(position)
                    Robot.MoveToAngle(roud, x_csv_offset, y_csv_offset)
                    
                    print("termination of the measurement process and performance of a new trance")
                    time.sleep(0.5)
                    break
            if len(position_mmaping) > 6:
                work = False
                print(" ------- ")
        print("saveing data ")
        SaveData.SaveToFile("measursment_list", measursment_list)

        SaveData.SaveToFile("position_mmaping", position_mmaping)
        
        
    except Exception as e:
        print("error: " + e)
        print("saveing data ")
        SaveData.SaveToFile("measursment_list", measursment_list)
        SaveData.SaveToFile("position_mmaping", position_mmaping)
        print("end of work")

        