import json
import matplotlib.pyplot as plt
import numpy as np

with open("data.json", "r") as f:
    data = json.load(f)

xs = []
series = {}
for index, d in enumerate(data):
    xs.append(index)
    for k, v in d.items():
        if not isinstance(v, str) and v is not None:
            if isinstance(v, list):
                v = v[-1]
            if k not in series:
                series[k] = []
            series[k].append(v)

print(series)

lines = []
for k in ['current_time']:
    v = series[k]
    lines.append(plt.plot(xs, v, label=k))
plt.legend(loc="upper left")
plt.show()
