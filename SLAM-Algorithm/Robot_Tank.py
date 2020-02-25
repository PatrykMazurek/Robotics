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


# def Stering():
#     global move, timeWork, direction, finish, work, callibration
#     print("Aktywacja wątka sterująceog")
#     while True:
#         if finish:
#             print("zakończenie wątka sterującego")
#             break
#         if move:
#             if direction == "cal" and work == False:
#                 while callibration == False:
#                     mR.reverse(speed+5)
#                     mL.forward(speed)
#                 StopForward()
#
#             if direction == "left" and work == False:
#                 if timeWork != 0:
#                     mL.reverse(speed)
#                     mR.forward(speed)
#                     time.sleep(timeWork)
#                     timeWork = 0
#
#                     direction = "forward"
#                     move = True
#                     work = False
#                 else:
#                     mL.reverse(speed)
#                     mR.forward(speed)
#                     move = False
#                     work = True
#             elif direction == "right"and work == False:
#                 if timeWork != 0:
#                     mL.forward(speed)
#                     mR.reverse(speed)
#                     time.sleep(timeWork)
#                     timeWork = 0
#                     StopForward()
#                     direction = "forward"
#                     move = True
#                     work = False
#                 else:
#                     mL.forward(speed)
#                     mR.reverse(speed)
#                     work = True
#                     move = False
#             elif direction == "forward"and work == False:
#                 work = True
#                 move = False
#                 #print(direction)
#                 #forward()
#             # elif direction == "patrol" and work == False:
#             #
#             #     # left
#             #     mL.reverse(speed)
#             #     mR.forward(speed)
#             #     oldTime = time.gmtime().tm_sec
#             #     while abs(oldTime - time.gmtime().tm_sec) < 5:
#             #         if faceD:
#             #             StopForward()
#             #             break
#             #
#             #
#
#             elif direction == "stop":
#                 work = False
#                 StopForward()
#     print("koniec pracy")



if __name__ == '__main__':
    try:

        # initalize importent object
        #th_stering = threading.Thread(target=Stering)
        #th_stering.start()
        measursment_list = []
        with open("compass-offset.csv", "r") as f:
            temp = f.readline().split(';')
            x_csv_offset = float(temp[0])
            y_csv_offset = float(temp[1])
        i = 0
        # Wykonanie pomiarów i określenie wstępnej pozycji robota
        position = Robot.TakeMeasurments(x_csv_offset, y_csv_offset)

        position_mmaping[i] = position
        old_x = 0.0
        old_y = 0.0
        measursment_list.append([old_x,old_y, 0.0, 0.0])

        roud = Robot.SpecityTheDirection(position_mmaping[i])
        print(roud)
        i = i + 1
        print("-- ustawianie robota --")
        print("kąt: " + str(roud))
        Robot.MoveToAngel(roud, x_csv_offset, y_csv_offset)
        # print(" --- pomiary ---")
        # print(position)
        work = True
        while work:
            start_dystans = Robot.sen.distance()
            Robot.start_Time = time.time()
            Robot.Forward()
            while True:
                # określenie dystansu od przeszkody
                if Robot.sen.distance() < 50:
                    Robot.StopForward()
                    Robot.end_Time = time.time()
                    # Robot.Revers()
                    # time.sleep(0.6)
                    # Robot.StopForward()
                    print("Rozpoczęcie nowych pomiarów")
                    time.sleep(0.5)
                    # określenie przebytej drogi
                    print("Nowa pozycja: ")
                    new_posittion = Compass.compass_angel(x_csv_offset, y_csv_offset)
                    print("Kąt: " + str(roud) )
                    print("Kąt po zatrzymaniu: " + str(new_posittion))
                    print("Oszacowanie dystansu:")
                    real_roud = Robot.DistanceToCheck()
                    #stop_distance = start_dystans - Robot.sen.distance()
                    # opkreśleni nowej pozycji pomiarów
                    print("pozycja x: " + str(old_x) + " y " + str(old_y))
                    new_x = real_roud * math.cos(np.radians(new_posittion)) + old_x
                    new_y = real_roud * math.sin(np.radians(new_posittion)) + old_y
                    print("pozycja x: " + str(new_x) + " y " + str(new_y))
                    # wykonanie pomiarów odległości
                    #input()
                    position = Robot.TakeMeasurments(x_csv_offset, y_csv_offset)
                    print(position)
                    position_mmaping[i] = position
                    measursment_list.append([new_x, new_y, real_roud, new_posittion])
                    old_x = new_x
                    old_y = new_y
                    i = i + 1
                    # wybranie nowej drogi
                    roud = Robot.SpecityTheDirection(position)
                    # skierowanie do nowej pozycji
                    Robot.MoveToAngel(roud, x_csv_offset, y_csv_offset)
                    #input()
                    print("Zakończenie procedury pomiarowej i wyznaczenie nowej trasy")
                    time.sleep(0.5)
                    break
            if len(position_mmaping) > 6:
                work = False
        with(open("measursment_list.txt", "w")) as f_m:
            f_m.write(str(measursment_list))

        with open("position_mmaping.txt", "w") as f_a:
            for maping in position_mmaping.items():
                f_a.write(str(maping))
    except Exception as e:
        print("awaryjne zakończenie pracy")
        print(e)
        with(open("measursment_list.txt", "w")) as f_m:
            f_m.write(str(measursment_list))

        with open("position_mmaping.txt", "w") as f_a:
            for maping in position_mmaping.items():
                f_a.write(str(maping))

    finally:
        print(" ----- ")
        print(measursment_list)
        print(" ----- ")
        print("zakończenie pracy")