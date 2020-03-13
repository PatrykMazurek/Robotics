import matplotlib.pyplot as plt
import numpy as np
import os

# method print the map with the position of the robot and landmarks 
def SaveMap(robotPoint, landmarks):
    nr = len(landmarks)
    p_x = []
    p_y = []
    m_x = []
    m_y = []
    
    for n in range(0, nr):
        p_x.append(robotPoint[n][0])
        p_y.append(robotPoint[n][1])
        for m in landmarks[n]:
            if m[1] > 0.0:
                m_x.append(m[1] * np.cos(np.radians(m[0])) + p_x[n])
                m_y.append(m[1] * np.sin(np.radians(m[0])) + p_y[n])
    plt.plot(p_x, p_y, "bx--")
    plt.plot(m_x, m_y, "ro")
    plt.grid()
    if os.path.exists("mapa.png"):
        os.remove("mapa.png")
    plt.savefig("mapa.png")

