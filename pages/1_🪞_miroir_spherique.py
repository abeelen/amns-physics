import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from numpy.polynomial.polynomial import polyfit, polyval

from common.items import draw_mirror
from common.utils import arrow_dxdy, draw_vertical_arrow


def get_sap(sa=0, ab=2, sc=0):
    sf = sc / 2

    if sa == sf:
        return np.sign(sa * sf) * np.inf

    sap = (sa * sf) / (sa - sf)

    return sap


def get_abp(sa=0, ab=2, sc=0, sap=None):
    if sap is None:
        sap = get_sap(sa=sa, ab=ab, sc=sc)

    if np.abs(sap) is np.inf:
        return np.inf

    if sa != 0:
        gamma = -sap / sa
    else:
        gamma = 1

    return gamma * ab


def draw_image(ax, sa=0, ab=2, sc=0, color="b"):
    sap = get_sap(sa, ab, sc)

    if sap is None:
        return None

    abp = get_abp(sa=sa, ab=ab, sc=sc, sap=sap)

    draw_vertical_arrow(
        ax, pos=sap, size=abp, label_bottom=r"$A^\prime$", label_head=r"$B^\prime$", color=color, virtual=sap > 0
    )


def draw_central_ray(ax, sa=0, ab=2, sc=0, scale=0.5, **kwargs):
    # Ray with goes to the center of the sphere

    line_kwargs = dict(c="r")
    line_kwargs.update(**kwargs)

    annotate_kwargs = dict(
        xycoords="data",
        textcoords="data",
        arrowprops=dict(
            arrowstyle=f"-|>, head_width={scale}, head_length={scale}",
            connectionstyle="arc3",
            edgecolor="r",
            facecolor="r",
        ),
    )
    annotate_kwargs["arrowprops"].update(**kwargs)

    line_kwargs = dict(c="r")
    if sa == sc:
        if sa > 0:
            line_kwargs["linestyle"] = "dashed"
        ax.axvline(sa, **line_kwargs)

        dx, dy = arrow_dxdy([sa, sc], [ab, 0], scale=scale)

        x, y = sa, ab + 0.3
        ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)
        x, y = sa, -0.3
        ax.annotate("", xy=(x, y), xytext=(x - dx, y - dy), **annotate_kwargs)

    else:
        x_min, x_max = ax.get_xlim()
        coeffs = polyfit([sa, sc], [ab, 0], 1)
        ax.plot([x_min, 0], polyval([x_min, 0], coeffs), **line_kwargs)  # real space
        ax.plot([0, x_max], polyval([0, x_max], coeffs), **line_kwargs, linestyle="dashed")  # virtual space

        dx, dy = arrow_dxdy([x_min, x_max], polyval([x_min, x_max], coeffs), scale=scale)
        # ax.arrow(-0.5, polyval(-0.5, coeffs), dx, dy, **arrow_kwargs)
        # ax.arrow(-np.abs(sa) - 1, polyval(-np.abs(sa) - 1, coeffs), -dx, -dy, **arrow_kwargs)

        x, y = -1, polyval(-1, coeffs)
        ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)
        x, y = -np.max(np.abs([sc, sa])) - 2, polyval(-np.max(np.abs([sc, sa])) - 2, coeffs)
        ax.annotate("", xy=(x, y), xytext=(x - dx, y - dy), **annotate_kwargs)


def draw_parallel_ray(ax, sa=0, ab=2, sc=0, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    annotate_kwargs = dict(
        xycoords="data",
        textcoords="data",
        arrowprops=dict(
            arrowstyle=f"-|>, head_width={scale}, head_length={scale}",
            connectionstyle="arc3",
            edgecolor="r",
            facecolor="r",
        ),
    )
    annotate_kwargs["arrowprops"].update(**kwargs)

    if sa < 0:
        ax.plot([sa, 0], [ab, ab], **line_kwargs)
    else:
        ax.plot([sa, 0], [ab, ab], **line_kwargs, linestyle="dashed")

    x, y = sa - np.sign(sa) * 1, ab
    dx, dy = np.sign(sa) * scale, 0
    ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)

    coeffs = polyfit([0, sc / 2], [ab, 0], 1)
    x_min, x_max = ax.get_xlim()
    ax.plot([0, x_min], polyval([0, x_min], coeffs), **line_kwargs)
    ax.plot([0, x_max], polyval([0, x_max], coeffs), **line_kwargs, linestyle="dashed")

    dx, dy = arrow_dxdy([x_min, x_max], polyval([x_min, x_max], coeffs), scale=scale)
    x, y = -1, polyval(-1, coeffs)
    ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)
    x, y = -np.max(np.abs([sc, sa])) - 2, polyval(-np.max(np.abs([sc, sa])) - 2, coeffs)
    ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)


def plot_figure(sc, sa, ab, image=False, parallel_ray=False, central_ray=False):
    fig, ax = plt.subplots()
    ax.set_aspect(3)
    ax.axhline(0, c="k", linewidth=2, linestyle="dashed")

    ax.scatter(0, 0, c="k")
    ax.text(1, -0.1, "S", horizontalalignment="center", verticalalignment="top")

    ax.set_xlim(-7, 7)
    ax.set_ylim(-2, 2)
    ax.set_axis_off()

    draw_mirror(ax, x=0, sc=sc)
    draw_vertical_arrow(ax, pos=sa, size=ab, virtual=sa > 0)

    if central_ray:
        draw_central_ray(ax, sa=sa, ab=ab, sc=sc)
    if parallel_ray:
        draw_parallel_ray(ax, sa=sa, ab=ab, sc=sc)

    if image:
        draw_image(ax, sa=sa, ab=ab, sc=sc)

    return fig


data_concave = {
    "SC [cm]": [-4] * 5,
    "SA [cm]": [-5, -1, -4, -3, -2],
    "AB [cm]": [+0.8] * 5,
}

data_convexe = {
    "SC [cm]": [4] * 6,
    "SA [cm]": [-2, +5, +4, +3, +2, +1],
    "AB [cm]": [+0.8] * 6,
}


st.set_page_config(page_title="Miroir Sphérique", page_icon="🪞")

st.title("Miroir Sphérique")

st.sidebar.write("Paramètres")
ab = st.sidebar.slider("AB [cm]", -1.0, 1.0, 0.5)
sa = st.sidebar.slider("SA [cm]", -10.0, 10.0, -5.0)
sc = st.sidebar.slider("SC [cm]", -10.0, 10.0, -4.0)

image = st.sidebar.checkbox("Image")
parallel_ray = st.sidebar.checkbox("Parallel")
central_ray = st.sidebar.checkbox("Centre")

mirror_type = st.selectbox("Type de miroir", ["Concave", "Convexe"], index=0, label_visibility="collapsed")
if mirror_type == "Concave":
    data = pd.DataFrame(data_concave)
elif mirror_type == "Convexe":
    data = pd.DataFrame(data_convexe)

event = st.dataframe(data, on_select="rerun", selection_mode="single-row")

if len(event.selection["rows"]):
    selected_row = event.selection["rows"][0]
    ab = data.iloc[selected_row]["AB [cm]"]
    sa = data.iloc[selected_row]["SA [cm]"]
    sc = data.iloc[selected_row]["SC [cm]"]


fig = plot_figure(sc, sa, ab, image, parallel_ray, central_ray)
st.pyplot(fig)


sap = get_sap(sa=sa, ab=ab, sc=sc)
abp = get_abp(sa=sa, ab=ab, sc=sc, sap=sap)

col1, col2, col3, col4 = st.columns(4)

col1.metric("SF [cm]", f"{sc / 2:4.3f}")
col2.metric("SA' [cm]", f"{sap:4.3f}")
col3.metric("A'B' [cm]", f"{abp:4.3f}")
col4.metric("gamma", f"{-sap / sa:4.3f}" if sap is not None else " ")
