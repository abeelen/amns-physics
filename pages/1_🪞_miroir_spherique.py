import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from numpy.polynomial.polynomial import polyfit, polyval

from common.items import draw_mirror
from common.utils import arrow_dxdy, draw_vertical_arrow

st.set_page_config(page_title="Miroir Sphérique", page_icon="📈")

st.title("Miroir Sphérique")

ab = st.sidebar.slider("AB [cm]", -10.0, 10.0, 5.0)
sa = st.sidebar.slider("SA [cm]", -10.0, 10.0, -5.0)
sc = st.sidebar.slider("SC [cm]", -10.0, 10.0, -4.0)

image = st.sidebar.checkbox("Image")
parallel_ray = st.sidebar.checkbox("Parallel")
central_ray = st.sidebar.checkbox("Centre")


def draw_image(ax, sa=0, ab=2, sc=0, color="b"):
    sf = sc / 2

    if sa == sf:
        return

    sap = (sa * sf) / (sa - sf)

    if sa != 0:
        gamma = -sap / sa
    else:
        gamma = 1
    abp = gamma * ab

    draw_vertical_arrow(
        ax, pos=sap, size=abp, label_bottom=r"$A^\prime$", label_head=r"$B^\prime$", color=color, virtual=sap > 0
    )


def draw_central_ray(ax, sa=0, ab=2, sc=0, scale=0.5, **kwargs):
    # Ray with goes to the center of the sphere

    line_kwargs = dict(c="r")
    line_kwargs.update(**kwargs)
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    line_kwargs = dict(c="r")
    if sa == sc:
        if sa > 0:
            line_kwargs["linestyle"] = "dashed"
        ax.axvline(sa, **line_kwargs)

        dx, dy = arrow_dxdy([sa, sc], [ab, 0], scale=scale)

        ax.arrow(sa, ab + 2, dx, dy, **arrow_kwargs)
        ax.arrow(sa, -2, -dx, -dy, **arrow_kwargs)

    else:
        x_min, x_max = ax.get_xlim()
        coeffs = polyfit([sa, sc], [ab, 0], 1)
        ax.plot([x_min, 0], polyval([x_min, 0], coeffs), **line_kwargs)  # real space
        ax.plot([0, x_max], polyval([0, x_max], coeffs), **line_kwargs, linestyle="dashed")  # virtual space

        dx, dy = arrow_dxdy([x_min, x_max], polyval([x_min, x_max], coeffs), scale=scale)

        ax.arrow(-0.5, polyval(-0.5, coeffs), dx, dy, **arrow_kwargs)
        ax.arrow(-np.abs(sa) - 1, polyval(-np.abs(sa) - 1, coeffs), -dx, -dy, **arrow_kwargs)


def draw_parallel_ray(ax, sa=0, ab=2, sc=0, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    if sa < 0:
        ax.plot([sa, 0], [ab, ab], **line_kwargs)
    else:
        ax.plot([sa, 0], [ab, ab], **line_kwargs, linestyle="dashed")

    ax.arrow(sa - np.sign(sa) * 1, ab, -np.sign(sa) * scale, 0, **arrow_kwargs)

    coeffs = polyfit([0, sc / 2], [ab, 0], 1)
    x_min, x_max = ax.get_xlim()
    ax.plot([0, x_min], polyval([0, x_min], coeffs), **line_kwargs)
    ax.plot([0, x_max], polyval([0, x_max], coeffs), **line_kwargs, linestyle="dashed")

    dx, dy = arrow_dxdy([x_min, x_max], polyval([x_min, x_max], coeffs), scale=scale)
    ax.arrow(-0.5, polyval(-0.5, coeffs), -dx, -dy, **arrow_kwargs)
    ax.arrow(-np.abs(sa) - 1, polyval(-np.abs(sa) - 1, coeffs), -dx, -dy, **arrow_kwargs)


fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.axhline(0, c="k", linewidth=2, linestyle="dashed")

ax.scatter(0, 0, c="k")
ax.text(1, -0.5, "S", horizontalalignment="center", verticalalignment="top")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_axis_off()

draw_mirror(ax, x=0, sc=sc)
draw_vertical_arrow(ax, pos=sa, size=ab, virtual=sa > 0)

if central_ray:
    draw_central_ray(ax, sa=sa, ab=ab, sc=sc)
if parallel_ray:
    draw_parallel_ray(ax, sa=sa, ab=ab, sc=sc)

if image:
    draw_image(ax, sa=sa, ab=ab, sc=sc)

st.pyplot(fig)
