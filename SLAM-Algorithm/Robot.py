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
    print("Szacowany przejechany dystans: " + str(realDistance))
    return realDistance

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
            print("kierunek między: " + str(tab_direction[i-1][0]) + " a " + str(tab_direction[i][0]))
    return direction

def TakeMeasurments(x_offset, y_offset):
    # lokalizacja podzielona na 12 stref co 30 stopni
    sector_range = 12
    angle_value = 30
    sector_executed = float(6)
    list_point = np.zeros((sector_range,2))
    table_range = np.arange(0, 361, sector_range)
    # określenie strefy w której znajduje się robot
    start_position = Compass.compass_angel(x_offset, y_offset)
    print("Pozycja początkowa: " + str(start_position))
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
                        scan_position = Compass.compass_angel(x_offset, y_offset)
                        # print("kąt: " + str(scan_position))
                        distance = sen.distance()
                        # print("dystans: " + str(distance))
                        if distance > float(450):
                            print("błędny pomiar: " + str(distance))
                            distance = float(0)
                        # [kąt, x, y]
                        # list_point[p] = [scan_position, (distance * math.cos(math.radians(scan_position))), (distance * math.sin(math.radians(scan_position)))]
                        list_point[p] = [scan_position, distance]
                        print(str(list_point[p]))
                        # input()

            if sector > 0:
                sector_range = sector;
                sector = 0
            else:
                break
        return list_point
    except Exception as e:
        print("błąd zakończenie pracy podczas wykonywania pomiarów")
        print(e)
        return list_point


# def lokalization(x_offset, y_offset):
#     # lokalizacja podzielona na 18 stref co 20 stopni
#     sector_range = 12
#     angle_value = 30
#     sector_executed = float(6)
#     list_point = np.zeros((sector_range,2))
#
#     # Określenie strefy w któej znajduje się robot
#     start_position = Compass.compass_angel(x_offset, y_offset)
#     print("Pozycja początkowa: " + str(start_position))
#     try:
#         for i in range(sector_range):
#             min_range = float(i * angle_value)
#             max_range = float(min_range + angle_value)
#             #print(str(min_range) + " - " + str(max_range))
#             if min_range < start_position < max_range:
#                 #print("Robot w przedziale nr: " + str(i))
#                 sector = i
#
#         while True:
#             for p in range(sector, sector_range):
#                 min_range = float(p * angle_value) + sector_executed
#                 max_range = float(min_range + angle_value) - sector_executed
#                 #print(str(min_range) + " - " + str(max_range))
#                 work = True
#                 TurnRight(35)
#                 while work:
#                     if  min_range < Compass.compass_angel(x_offset, y_offset) < max_range:
#                         StopForward()
#                         work = False
#                         scan_position = Compass.compass_angel(x_offset, y_offset)
#                         print("kąt: "+ str(scan_position))
#                         distance = sen.distance()
#                         print("dystans: " + str(distance))
#                         if distance > float(400):
#                             print("błędny pomiar: " + str(distance))
#                             distance = float(0)
#                         # [kąt, x, y]
#                         #list_point[p] = [scan_position, (distance * math.cos(math.radians(scan_position))), (distance * math.sin(math.radians(scan_position)))]
#                         list_point[p] = [scan_position, distance]
#                         print(str(list_point[p]))
#                         #input()
#                         #print(str(scan_position))
#
#             if sector > 0:
#                 sector_range = sector;
#                 sector = 0
#             else:
#                 break
#         # usuwanie odległości które są szumem
#         return list_point
#     except Exception as e:
#         print("błąd zakończenie pracy podczas wykonywania pomiarów")
#         print(e)
#         return list_point

def MoveToAngel(angle, x_offset, y_offset):
    # ustawienie robota w odpowiednim kierunku
    sector_range = 12
    angle_value = 30
    sector_executed = 7.5
    start_position = Compass.compass_angel(x_offset, y_offset)
    position = start_position/2
    print("Z pozycji: " + str(start_position))
    print("Ustawiam się na kierunek: " + str(angle))
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
    print("Dystans do przejechania " + str(d))
    return "forward"

# tymczasowa funkcja
def SetDirection(x_offset, y_offset):
    try:
        while True:
            print("Pozycja robota: " + str(Compass.compass_angel(x_offset, y_offset)))
            d = input("Podaj kierunek: ")
            s = d.split(' ')
            sector_executed = 7.5
            min_range = float(s[1]) - sector_executed
            max_range = float(s[1]) + sector_executed
            while True:
                if s[0] == 'L':
                    TurnLeft(35)
                    if min_range < Compass.compass_angel(x_offset, y_offset) < max_range:
                        StopForward()
                        break
                else:
                    TurnRight(35)
                    if min_range < Compass.compass_angel(x_offset, y_offset) < max_range:
                        StopForward()
                        break
            position = Compass.compass_angel(x_offset, y_offset)
            print("Pozycja robota: " + str(position))
            if input("Czy kierunek idealny? t/n ") == 't':
                print("Wyjście z funkcji")
                return position
    except Exception as e:
        print(e)
        print("Problem zakończenie programu")