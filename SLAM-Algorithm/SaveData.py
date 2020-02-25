import numpy as np

def SaveToFile(fileName, date):
    with(open(fileName+".txt", "w")) as f:
        if fileName == "measursment_list":
            for i in date:
                f.write(str(i[0]) + " " + str(i[1])+ " " + str(i[2]) + " " + str(i[3])+ "\n")
        else:
            nr = len(date)
            for i in range(0, nr):
                for d in date[i]:
                    f.write(str(d[0]) + " " + str(d[1])+ ";")
                f.write("\n")

def ReadFromFile(fileName, location):
    with(open(location + "\\" + fileName + ".txt", "r")) as f:
        point_x = []
        point_y = []
        if fileName == "measursment_list":
            for line in f:
                temp = line.split(' ')
                point_x.append(temp[0])
                point_y.append(temp[1])
                print(line)
            return point_x, point_y
        else:
            for line in f:
                temp = line.split(';')
                for point in temp:
                    res = point.split(' ')
                    point_x.append(res[1] * np.cos(np.radians(res[0])) + p_x[nr])
                    point_y.append(res[1] * np.sin(np.radians(res[0])) + p_y[nr])
