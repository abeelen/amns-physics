import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from numpy.polynomial.polynomial import polyfit, polyval

from common.items import draw_lens
from common.utils import arrow_dxdy, draw_vertical_arrow


def get_oap(oa=0, of=0):
    # 1 / OAp - 1/ OA = 1/OFp
    ofp = -of
    if of == oa:
        return np.sign(of * oa) * np.inf
    oap = ofp * oa / (ofp + oa)
    return oap


def get_abp(oa=0, ab=2, of=None, oap=None):
    if oap is None:
        oap = get_oap(oa=oa, of=of)

    if np.isinf(oap):
        return np.inf

    if oa != 0:
        gamma = oap / oa
    else:
        gamma = 1

    abp = gamma * ab
    return abp


def draw_image(ax, oa=0, ab=2, of=0, color="b"):
    oap = get_oap(oa=oa, of=of)
    abp = get_abp(oa=oa, ab=ab, of=of, oap=oap)

    draw_vertical_arrow(
        ax, pos=oap, size=abp, label_bottom=r"$A^\prime$", label_head=r"$B^\prime$", color=color, virtual=oap < 0
    )


def draw_parallel_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")

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

    x_min, x_max = ax.get_xlim()

    coeffs = polyfit([0, -of], [ab, 0], 1)

    if oa < 0:
        ax.plot([oa, 0, x_max], [ab, ab, polyval(x_max, coeffs)], **line_kwargs)

        x, y = oa / 2, ab
        dx, dy = np.sign(oa) * scale, 0
        ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)

        x, y = (np.min(np.abs([oa, of])) / 2, polyval(np.min(np.abs([oa, of])) / 2, coeffs))
        dx, dy = arrow_dxdy([0, -of], [ab, 0], scale=scale)
        ax.annotate("", xy=(x, y), xytext=(x - np.sign(oa * of) * dx, y - np.sign(oa * of) * dy), **annotate_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)

        if of > 0:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)

    else:
        ax.plot([oa, 0], [ab, ab], **line_kwargs, linestyle="dashed")
        ax.plot([x_min, 0, x_max], [ab, ab, polyval(x_max, coeffs)], **line_kwargs)

        x, y = (np.abs(of) * 3 / 2, polyval(np.abs(of) * 3 / 2, coeffs))
        dx, dy = arrow_dxdy([0, -of], [ab, 0], scale=scale)
        ax.annotate("", xy=(x, y), xytext=(x + np.sign(oa * of) * dx, y + np.sign(oa * of) * dy), **annotate_kwargs)

        x, y = -np.abs(of) / 2, ab
        dx, dy = -np.sign(oa) * scale, 0
        ax.annotate("", xy=(x, y), xytext=(x + dx, y + dy), **annotate_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([x_min, 0], coeffs), linestyle="dashed", **line_kwargs)


def draw_focal_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")

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

    x_min, x_max = ax.get_xlim()

    if oa == of:
        return

    coeffs = polyfit([oa, of], [ab, 0], 1)
    if oa < 0:
        ax.plot([oa, 0, x_max], [ab, polyval(0, coeffs), polyval(0, coeffs)], **line_kwargs)

        x, y = oa / 2, polyval(oa / 2, coeffs)
        dx, dy = arrow_dxdy([oa, 0], [ab, polyval(0, coeffs)], scale=scale)
        ax.annotate("", xy=(x, y), xytext=(x - dx, y - dy), **annotate_kwargs)

        x, y = x_max / 2, polyval(0, coeffs)
        dx, dy = scale, 0
        ax.annotate("", xy=(x, y), xytext=(x - dx, y - dy), **annotate_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), **line_kwargs, linestyle="dashed")

        if of > 0:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), linestyle="dashed", **line_kwargs)

    else:
        ax.plot([x_min, 0], polyval([x_min, 0], coeffs), **line_kwargs)
        x, y = -np.abs(of) / 2, polyval(-np.abs(of) / 2, coeffs)
        dx, dy = arrow_dxdy([x_min, oa], [polyval(x_min, coeffs), ab], scale=scale)

        ax.annotate("", xy=(x, y), xytext=(x - np.sign(oa) * dx, y - np.sign(oa) * dy), **annotate_kwargs)

        ax.plot([oa, 0], [ab, polyval(0, coeffs)], **line_kwargs, linestyle="dashed")
        ax.plot([0, x_max], polyval([0, 0], coeffs), **line_kwargs)

        x, y = np.abs(of) * 3 / 2, polyval(0, coeffs)
        dx, dy = scale, 0
        ax.annotate("", xy=(x, y), xytext=(x - np.sign(oa) * dx, y - np.sign(oa) * dy), **annotate_kwargs)

        if oa > of:
            ax.plot([x_min, 0], polyval([0, 0], coeffs), linestyle="dashed", **line_kwargs)


def draw_central_ray(ax, oa=-3, of=-2, ab=2, scale=0.5, **kwargs):
    line_kwargs = dict(c="r")

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

    x_min, x_max = ax.get_xlim()

    coeffs = polyfit([oa, 0], [ab, 0], 1)

    if oa < 0:
        ax.plot([oa, x_max], polyval([oa, x_max], coeffs), **line_kwargs)
        if oa > of:
            ax.plot([x_min, oa], polyval([x_min, oa], coeffs), linestyle="dashed", **line_kwargs)
    else:
        ax.plot([x_min, x_max], polyval([x_min, x_max], coeffs), **line_kwargs)

    x, y = -np.abs(oa) / 2, polyval(-np.abs(oa) / 2, coeffs)
    dx, dy = arrow_dxdy([oa, 0], [ab, 0], scale=scale)
    ax.annotate("", xy=(x, y), xytext=(x + np.sign(oa) * dx, y + np.sign(oa) * dy), **annotate_kwargs)


def plot_figure(of, oa, ab, parallel_ray=False, central_ray=False, focal_ray=False, image=False):
    fig, ax = plt.subplots()
    ax.set_aspect(2)
    ax.axhline(0, c="k", linewidth=2, linestyle="dashed")

    ax.scatter(0, 0, c="k")
    ax.text(1, -0.5, "O", horizontalalignment="center", verticalalignment="top")

    ax.set_xlim(-6.5, 7)
    ax.set_ylim(-2, 2)
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

    return fig


data_convergente = {
    "OF' [cm]": [+2] * 6,
    "OA [cm]": [-4.0, -1.0, -3, -2.0, +1, +2],
    "AB [cm]": [+0.8] * 6,
}
data_divergente = {
    "OF' [cm]": [-2] * 6,
    "OA [cm]": [-3, -2, -1, +3, +2, +1],
    "AB [cm]": [+0.8] * 6,
}

st.set_page_config(page_title="Lentilles Minces", page_icon="🔎")

st.title("Lentilles minces")

st.sidebar.write("Paramètres")

of = st.sidebar.slider("OF [cm]", -5.0, 5.0, -2.0)
oa = st.sidebar.slider("OA [cm]", -5.0, 5.0, -4.0)
ab = st.sidebar.slider("AB [cm]", -1.0, 1.0, 0.8)

image = st.sidebar.checkbox("Image")
parallel_ray = st.sidebar.checkbox("Parallel")
central_ray = st.sidebar.checkbox("Centre")
focal_ray = st.sidebar.checkbox("Focale")

with st.expander('Preréglages'):

    lens_type = st.selectbox("Type de lentilles", ["Convergente", "Divergente"], index=0, label_visibility="collapsed")
    if lens_type == "Convergente":
        data = pd.DataFrame(data_convergente)
    elif lens_type == "Divergente":
        data = pd.DataFrame(data_divergente)

    event = st.dataframe(data, on_select="rerun", selection_mode="single-row")

if len(event.selection["rows"]):
    selected_row = event.selection["rows"][0]
    of = -data.iloc[selected_row]["OF' [cm]"]
    oa = data.iloc[selected_row]["OA [cm]"]
    ab = data.iloc[selected_row]["AB [cm]"]

fig = plot_figure(of, oa, ab, parallel_ray=parallel_ray, focal_ray=focal_ray, central_ray=central_ray, image=image)
st.pyplot(fig)

oap = get_oap(oa=oa, of=of)
abp = get_abp(oa=oa, ab=ab, of=of, oap=oap)

col1, col2, col3 = st.columns(3)
col1.metric(r"$OA^\prime$ [cm]", f"{oap:4.3f}")
col2.metric(r"$A^{\prime}B^{\prime}$ [cm]", f"{abp:4.3f}")
col3.metric(r"$\gamma$", f"{oap / oa:4.3f}")
