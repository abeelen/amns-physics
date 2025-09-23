import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from numpy.polynomial.polynomial import polyfit, polyval

from common.items import draw_lens
from common.utils import arrow_dxdy, draw_vertical_arrow

st.set_page_config(page_title="Lentilles Minces", page_icon="🔎")

st.title("Lentilles minces")

st.sidebar.header("Lentilles minces")
st.sidebar.write("Paramètres")


of = st.sidebar.slider("OF [cm]", -10.0, 10.0, -5.0)
oa = st.sidebar.slider("OA [cm]", -10.0, 10.0, -7.0)
ab = st.sidebar.slider("AB [cm]", -5.0, 5.0, 2.5)

image = st.sidebar.checkbox("Image")
parallel_ray = st.sidebar.checkbox("Parallel")
central_ray = st.sidebar.checkbox("Centre")
focal_ray = st.sidebar.checkbox("Focale")


def draw_image(ax, oa=0, ab=2, of=0, color="b"):
    # 1 / OAp - 1/ OA = 1/OFp

    ofp = -of
    oap = ofp * oa / (ofp + oa)

    if oa != 0:
        gamma = oap / oa
    else:
        gamma = 1

    abp = gamma * ab
    st.write(f"$\gamma = ${gamma:3.2f}")
    draw_vertical_arrow(
        ax, pos=oap, size=abp, label_bottom=r"$A^\prime$", label_head=r"$B^\prime$", color=color, virtual=oap < 0
    )


def draw_parallel_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    x_min, x_max = ax.get_xlim()

    coeffs = polyfit([0, -of], [ab, 0], 1)

    if oa < 0:
        ax.plot([oa, 0, x_max], [ab, ab, polyval(x_max, coeffs)], **line_kwargs)

        dx, dy = arrow_dxdy([0, -of], [ab, 0], scale=scale)
        ax.arrow(oa / 2, ab, -np.sign(oa) * scale, 0, **arrow_kwargs)
        ax.arrow(
            np.abs(oa) / 2,
            polyval(np.abs(oa) / 2, coeffs),
            np.sign(oa) * np.sign(of) * dx,
            np.sign(oa) * np.sign(of) * dy,
            **arrow_kwargs,
        )
        if oa > of:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)

        if of > 0:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)

    else:
        ax.plot([oa, 0], [ab, ab], **line_kwargs, linestyle="dashed")
        ax.plot([x_min, 0, x_max], [ab, ab, polyval(x_max, coeffs)], **line_kwargs)
        dx, dy = arrow_dxdy([0, -of], [ab, 0], scale=scale)
        ax.arrow(
            np.abs(of) * 3 / 2,
            polyval(np.abs(of) * 3 / 2, coeffs),
            -np.sign(oa) * np.sign(of) * dx,
            -np.sign(oa) * np.sign(of) * dy,
            **arrow_kwargs,
        )
        ax.arrow(-np.abs(of) / 2, ab, np.sign(oa) * scale, 0, **arrow_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)


def draw_focal_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    x_min, x_max = ax.get_xlim()

    coeffs = polyfit([oa, of], [ab, 0], 1)

    if oa < 0:
        ax.plot([oa, 0, x_max], [ab, polyval(0, coeffs), polyval(0, coeffs)], **line_kwargs)

        dx, dy = arrow_dxdy([oa, 0], [ab, polyval(0, coeffs)], scale=scale)
        ax.arrow(oa / 2, polyval(oa / 2, coeffs), dx, dy, **arrow_kwargs)
        ax.arrow(x_max / 2, polyval(0, coeffs), scale, 0, **arrow_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), **line_kwargs, linestyle="dashed")

        if of > 0:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), linestyle="dashed", **line_kwargs)

    else:
        ax.plot([x_min, 0], polyval([x_min, 0], coeffs), **line_kwargs)
        dx, dy = arrow_dxdy([x_min, oa], [polyval(x_min, coeffs), ab], scale=scale)
        ax.arrow(
            -np.abs(of) / 2,
            polyval(-np.abs(of) / 2, coeffs),
            np.sign(oa) * dx,
            np.sign(oa) * dy,
            **arrow_kwargs,
        )

        ax.plot([oa, 0], [ab, polyval(0, coeffs)], **line_kwargs, linestyle="dashed")
        ax.plot([0, x_max], polyval([0, 0], coeffs), **line_kwargs)

        ax.arrow(np.abs(of) * 3 / 2, polyval(0, coeffs), scale, 0, **arrow_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), linestyle="dashed", **line_kwargs)


def draw_central_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")
    arrow_kwargs = dict(shape="full", lw=0, length_includes_head=True, head_width=scale, color="r")
    arrow_kwargs.update(**kwargs)

    x_min, x_max = ax.get_xlim()

    coeffs = polyfit([oa, 0], [ab, 0], 1)
    dx, dy = arrow_dxdy([oa, 0], [ab, 0], scale=scale)

    if oa < 0:
        ax.plot([oa, x_max], polyval([oa, x_max], coeffs), **line_kwargs)
        if oa > of:
            ax.plot([x_min, oa], polyval([x_min, oa], coeffs), linestyle="dashed", **line_kwargs)
    else:
        ax.plot([x_min, x_max], polyval([x_min, x_max], coeffs), **line_kwargs)

    ax.arrow(-np.abs(oa) / 2, polyval(-np.abs(oa) / 2, coeffs), -np.sign(oa) * dx, -np.sign(oa) * dy, **arrow_kwargs)

    # ax.arrow(np.abs(oa) / 2, polyval(np.abs(oa) / 2, coeffs), -np.sign(oa) * dx, -np.sign(oa) * dy, **arrow_kwargs)


fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.axhline(0, c="k", linewidth=2, linestyle="dashed")

ax.scatter(0, 0, c="k")
ax.text(1, -0.5, "O", horizontalalignment="center", verticalalignment="top")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_axis_off()

draw_vertical_arrow(ax, pos=oa, size=ab, virtual=oa > 0)
draw_lens(ax, of=of)
if parallel_ray:
    draw_parallel_ray(ax, oa=oa, of=of, ab=ab)
if focal_ray:
    draw_focal_ray(ax, oa=oa, of=of, ab=ab)
if central_ray:
    draw_central_ray(ax, oa=oa, of=of, ab=ab)
if image:
    draw_image(ax, oa=oa, of=of, ab=ab)

st.pyplot(fig)
