import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from common.utils import arrow_dxdy, draw_angle

min_n = 1.0
max_n = 2.0

cmap = plt.colormaps.get_cmap("Blues")
norm = colors.Normalize(min_n, max_n)


def get_ilim(n1, n2):
    i_lim = np.nan
    if n2 < n1:
        i_lim = np.degrees(np.asin(n2 / n1))
    return i_lim


def get_i2(i1, n1, n2, i_lim=None):
    if i_lim is None:
        i_lim = get_ilim(n1, n2)

    i2 = i1
    if not np.isnan(i_lim) and i1 > i_lim:
        i2 = np.nan
    if (not np.isnan(i_lim) and i1 < i_lim) or (n2 > n1):
        i2 = np.degrees(np.asin(n1 / n2 * np.sin(np.radians(i1))))
    return i2


def draw_arrow(ax, xs, ys, scale=0.05, **kwargs):
    dx, dy = arrow_dxdy(xs, ys, scale=scale)
    x_arrow = np.mean(xs)
    y_arrow = np.mean(ys)

    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=0.05)
    arrow_kwargs.update(**kwargs)
    ax.arrow(x_arrow, y_arrow, dx, dy, **arrow_kwargs)


def plot_figure(i1, n1, n2, i2=None, i_lim=None, radius=np.sqrt(2)):
    if i2 is None:
        i2 = get_i2(i1, n1, n2)

    if i_lim is None:
        i_lim = get_ilim(n1, n2)

    input_ray = [-radius * np.sin(np.radians(i1)), 0], [radius * np.cos(np.radians(i1)), 0]
    refracted_ray = [0, radius * np.sin(np.radians(i2))], [0, -radius * np.cos(np.radians(i2))]
    reflected_ray = [0, radius * np.sin(np.radians(i1))], [0, radius * np.cos(np.radians(i1))]

    limit_ray = (
        [-np.sign(i1 + 1e-12) * radius * np.sin(np.radians(np.abs(i_lim))), 0],
        [radius * np.cos(np.radians(i_lim)), 0],
    )

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.fill_between([-1, 1], 0, 1, color=cmap(norm(n1)), alpha=0.5)
    ax.fill_between([-1, 1], -1, 0, color=cmap(norm(n2)), alpha=0.5)
    ax.axhline(0, c="k", linewidth=2)
    ax.axvline(0, c="k", linewidth=1, linestyle="dashed")
    ax.scatter(0, 0, s=50, c="k")
    ax.plot(*limit_ray, c="k", linestyle="dotted")

    text_kwargs = dict(verticalalignment="center")
    ax.text(-0.9, 0.1, "$n_1$", **text_kwargs)
    ax.text(-0.9, -0.1, "$n_2$", **text_kwargs)

    # incoming ray
    ax.plot(*input_ray, c="r")
    draw_arrow(ax, *input_ray, color="r")
    draw_angle(ax, i1, color="r")

    ax.plot(*refracted_ray, c="g")
    draw_arrow(ax, *refracted_ray, color="g")
    draw_angle(ax, i2, top=False, color="g")

    if not np.isnan(i_lim) and np.abs(i1) >= np.abs(i_lim):
        ax.plot(*reflected_ray, c="r")
        draw_arrow(ax, *reflected_ray, color="r")
        draw_angle(ax, -i1, radius=0.8, color="r")

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_axis_off()

    return fig


data = {"n1": [1, 1.5, 1.5], "n2": [1.5, 1, 1], "i1 [°]": [45, 30, 41.5]}
data = pd.DataFrame(data)

st.set_page_config(page_title="Dioptre Plan", page_icon="📐")

st.title("Dioptre plan")

st.sidebar.write("Paramètres")

n1 = st.sidebar.slider(r"$n_1$", min_n, max_n)
n2 = st.sidebar.slider(r"$n_2$", min_n, max_n)
i1 = st.sidebar.slider(r"$i_1$", 0, 90, 30)

event = st.dataframe(data, on_select="rerun", selection_mode="single-row")

if len(event.selection["rows"]):
    selected_row = event.selection["rows"][0]
    n1 = data.iloc[selected_row]["n1"]
    n2 = data.iloc[selected_row]["n2"]
    i1 = data.iloc[selected_row]["i1 [°]"]

i_lim = get_ilim(n1, n2)
i2 = get_i2(i1, n1, n2)

fig = plot_figure(i1, n1, n2, i2=i2, i_lim=i_lim)
if n1 > n2:
    i_lim_label = r"$\mid \theta_{lim} \mid$ "
    st.write(r"$n_2 < n_1  \Rightarrow\, \mid \theta_{lim} \mid = $" + f"{i_lim:3.2f}°")
else:
    st.write("$n_2 > n_1$")
st.pyplot(fig)

col1, col2, col3 = st.columns(3)
col1.metric(r"$sin(i_1)$", f"{np.sin(np.radians(i1)):4.2f}")
col2.metric(r"$sin(i_2)$", f"{np.sin(np.radians(i2)):4.2f}")
col3.metric(r"$i_2 [°]$", f"{i2:4.2f}")
