import numpy as np
from matplotlib import patches


def draw_vertical_arrow(ax, pos=0, size=2, color="k", label_bottom="A", label_head="B", virtual=False):
    arrow_kwargs = dict(length_includes_head=True, head_width=0.5, head_length=0.5, color=color)
    text_kwargs = dict(horizontalalignment="center", color=color)

    x_min, x_max = ax.get_xlim()
    if pos < x_min or pos > x_max:
        return

    if virtual:
        arrow_kwargs["linestyle"] = "dotted"
    ax.arrow(pos, 0, dx=0, dy=size, **arrow_kwargs)

    ax.text(pos, -np.sign(size) * 0.8, label_bottom, verticalalignment="top", **text_kwargs)
    y_min, y_max = ax.get_ylim()
    if size < y_min or size > y_max:
        return
    ax.text(pos, size + np.sign(size) * 0.8, label_head, verticalalignment="bottom", **text_kwargs)


def arrow_dxdy(xs, ys, scale=0.05):
    dx = np.diff(xs).astype(float)
    dy = np.diff(ys).astype(float)

    norm = np.hypot(dx, dy)
    if norm == 0:  # Degenerate case: both points are the same
        return None
    dx /= norm
    dy /= norm

    # Scale the arrow length
    dx *= scale
    dy *= scale

    return float(dx), float(dy)


def draw_angle(ax, angle, top=True, radius=1, **kwargs):
    if np.isnan(angle):
        return

    if top:
        start = 90
    else:
        start = -90

    if angle > 0:
        arc = patches.Arc((0, 0), radius, radius, angle=start, theta1=0, theta2=angle, **kwargs)
    else:
        arc = patches.Arc((0, 0), radius, radius, angle=start, theta1=angle, theta2=0, **kwargs)

    ax.add_patch(arc)
