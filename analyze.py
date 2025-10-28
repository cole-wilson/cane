import matplotlib.pyplot as plt
import numpy as np
import sys

xs = []
bws = []
ress = []

old = 0

with open(sys.argv[1], "r") as f:
    header_line = f.readline().strip().split(",")
    print(header_line)
    T_COL = header_line.index("t")
    BW_COL = header_line.index("bandwidth")
    RES_COL = header_line.index("yt_sfn_connection_speed")

    c = 0
    while True:
        try:
            line = f.readline().strip().split(",")
            # print(line)
            bws.append(float(line[BW_COL]))
            r = float(line[RES_COL])
            if r == 0: r = old
            old = r
            ress.append(r)
            xs.append(c)
            c += 1
        except EOFError:
            break
        except IndexError:
            # print("index error at", c)
            break

fig, ax1 = plt.subplots()
ax1.plot(xs, bws, label="bandwidth")
ax2 = ax1.twinx()
ax2.plot(xs, ress, label="yt connection speed", color="red")
ax2.legend(loc="upper right")
ax1.legend(loc="upper left")
plt.show()
