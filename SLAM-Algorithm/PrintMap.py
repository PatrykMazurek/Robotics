import matplotlib.pyplot as plt
import numpy as np
import os

def SaveMap(robotPoint, landmarks):
    nr = len(landmarks)
    print(str(len(robotPoint)))
    print(str(len(landmarks)))
    p_x = []
    p_y = []
    m_x = []
    m_y = []
    room_x = np.array([0, 180, 180, 130, 130, 180, 180, -100, -100, -220, -220, 0, 0])
    room_y = np.array([0, 0, -230, -230, -310, -310, -560, -560, -420, -420, -270, -270, 0])

    # pierwsza próba
    # room_x = room_x - 100
    # room_y = room_y + 100

    # druda próba
    room_x = room_x - 90
    room_y = room_y + 460

    for n in range(0, nr):
        p_x.append(robotPoint[n][0])
        p_y.append(robotPoint[n][1])
        for m in landmarks[n]:
            if m[1] > 0.0:
                m_x.append(m[1] * np.cos(np.radians(m[0])) + p_x[n])
                m_y.append(m[1] * np.sin(np.radians(m[0])) + p_y[n])
    plt.plot(p_x, p_y, "bx--")
    plt.plot(m_x, m_y, "ro")
    plt.plot(room_x, room_y)
    plt.grid()
    if os.path.exists("mapa.png"):
        print("plik istnieje usuwa go")
        os.remove("mapa.png")
    plt.savefig("mapa.png")

