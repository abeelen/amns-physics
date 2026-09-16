import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title("Période Temporelle")

st.sidebar.write("Paramètres")

n_frame = 30
n_period = 3

timer_x = 0.15
timer_y = 0.9
timer_radius = 0.025

x = np.linspace(0, n_period * 2 * np.pi, 200)
y = np.cos(x)

x_label = np.arange(n_period + 1) * 2 * np.pi
y_label = np.cos(x_label)
t_label = [f"$M_{i}$" for i in np.arange(1, n_period + 2)]

fig, ax = plt.subplots()
ax.set_aspect(3)
ax.set_xlim(0, n_period * 2 * np.pi)
for _x in x_label:
    ax.axvline(_x, linestyle="dotted", c="r")


(line,) = ax.plot(x, y)
t_time = ax.text(timer_x, timer_y, "t = 0 T", horizontalalignment="center", transform=ax.transAxes)
scatter = ax.scatter(x_label, y_label, marker="+", c="r")
texts = [ax.text(_x, _y, _s, horizontalalignment="left", c="r") for _x, _y, _s in zip(x_label, y_label, t_label)]
(r_time,) = ax.plot(
    timer_x + timer_radius * np.cos(np.linspace(0, 2 * np.pi)),
    timer_y - 0.15 + timer_radius * ax.get_aspect() * np.sin(np.linspace(0, 2 * np.pi)),
    transform=ax.transAxes,
    c="k",
)

ax.set_axis_off()
st_plt = st.pyplot(fig)


def init():
    line.set_ydata(y)


def animate(i):
    delta_t = i * 2 * np.pi / n_frame
    line.set_ydata(np.cos(x + delta_t))
    y_label = np.cos(x_label + delta_t)
    scatter.set_offsets(np.array([x_label, y_label]).T)
    for t, _y in zip(texts, y_label):
        t.set_y(_y)

    t_time.set_text(f"t = {i / n_frame:3.2f} T")

    theta = np.linspace(np.pi / 2, np.pi / 2 - delta_t)
    r_time.set_xdata(timer_x + timer_radius * np.cos(theta))
    r_time.set_ydata(timer_y - 0.15 + timer_radius * ax.get_aspect() * np.sin(theta))
    st_plt.pyplot(fig)


init()
while True:
    for i in range(n_frame):
        animate(i)
        time.sleep(0.1)
