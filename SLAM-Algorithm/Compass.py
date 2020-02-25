import smbus, time, math
import os
bus = smbus.SMBus(1)
address = 0x1e
x_offset = 0
y_offset = 0
scale = 0.92

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low

    return val

def read_word_2c(adr):

    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

def compass_angel( x_csv_offset, y_csv_offset):
    write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000)  # Continuous sampling

    x_out = (read_word_2c(3) - x_csv_offset) * scale
    y_out = (read_word_2c(7) - y_csv_offset) * scale
    z_out = (read_word_2c(5)) * scale

    bearing = math.atan2(y_out, x_out)
    if (bearing < 0):
        bearing += 2 * math.pi
    #print("Bearing: ", bearing)
    return round(math.degrees(bearing), 3)

def calibrating(file_name):
    f = open(file_name+".dat", "a+")

    write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000)  # Continuous sampling

    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    for i in range(0, 500):
        x_out = read_word_2c(3)
        y_out = read_word_2c(7)
        z_out = read_word_2c(5)

        bearing = math.atan2(y_out, x_out)
        if (bearing < 0):
            bearing += 2 * math.pi
        f.writelines(str(x_out) +"," + str(y_out)+ "," + str(x_out * scale)+","+str(y_out * scale)+"\n")

        if x_out < minx:
            minx = x_out
        if y_out < miny:
            miny = y_out
        if x_out > maxx:
            maxx = x_out
        if y_out > maxy:
            maxy = y_out
        # print x_out, y_out, (x_out * scale), (y_out * scale)
        time.sleep(0.1)

    f.close()
    offset = open("compass-offset.csv", "w")
    print("minx: ", minx)
    print("miny: ", miny)
    print("maxx: ", maxx)
    print("maxy: ", maxy)
    print("x offset: ", (maxx + minx) / 2)
    print("y offset: ", (maxy + miny) / 2)
    x_offset = (maxx + minx) / 2
    y_offset = (maxy + miny) / 2
    offset.writelines(str(x_offset)+";"+str(y_offset))
    offset.close()
    # zakończenie procesu kalibracji
    return False