import numpy as np
from matplotlib import patches


def draw_mirror(ax, x=0, sc=-2, half_height=1):
    delta = np.sign(sc) * 0.5
    ax.plot([x + delta, x, x, x + delta], [half_height + 0.1, half_height, -half_height, -half_height - 0.1], c="k")
    ax.add_patch(
        patches.Rectangle(
            (x, -half_height),
            np.abs(delta),
            2 * half_height,
            fill=None,
            hatch="///",
            edgecolor=None,
            facecolor="k",
            linewidth=0,
        )
    )

    ax.scatter(sc, 0, c="k")
    ax.text(sc, -0.1, "C", horizontalalignment="center", verticalalignment="top")
    ax.scatter(sc / 2, 0, c="k")
    ax.text(sc / 2, -0.1, "F", horizontalalignment="center", verticalalignment="top")


def draw_lens(ax, x=0, of=-2, half_height=1.5, head_length=0.1, color="k"):
    # lens_kwargs = dict(arrowstyle='<->', color=color)
    # ax.annotate('', xy=(0, -5), xytext=(0, 5), arrowprops=lens_kwargs)
    # lens_kwargs = dict(head_length=5, head_width=2, widthA=1.0, widthB=1.0, lengthA=2, lengthB=0.2, angleA=0, angleB=0, scaleA=None, scaleB=None)

    # ax.add_patch(patches.FancyArrowPatch(posA=(0, -5), posB=(0, 5), color=color, arrowstyle=patches.ArrowStyle.CurveAB(**lens_kwargs)))

    ax.plot((0, 0), (-half_height, half_height), c="k")
    head = np.array([head_length, 0, head_length])
    ax.plot((-head_length, 0, head_length), -half_height - np.sign(of) * head, c="k")
    ax.plot((-head_length, 0, head_length), half_height + np.sign(of) * head, c="k")

    text_kwargs = dict(horizontalalignment="center", color=color)
    ax.plot([of, of], [-head_length, head_length], c="k")
    ax.text(of, -head_length, "F", verticalalignment="top", **text_kwargs)
    ax.plot([-of, -of], [-head_length, head_length], c="k")
    ax.text(-of, -head_length, "F$^\prime$", verticalalignment="top", **text_kwargs)
