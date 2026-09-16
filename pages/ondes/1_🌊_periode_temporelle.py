import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title("Période Temporelle")

st.sidebar.write("Paramètres")

T_AXIS = 5.0  # fenêtre temporelle affichée (s), fixe
Y_LIM = 2.3  # échelle des ordonnées, fixe (l'amplitude va de 0 à 2)

n_periods_options = list(range(10, 0, -1))  # de 10 (période courte) à 1 (période longue)
period = st.sidebar.select_slider("Période T (s)", options=[T_AXIS / k for k in n_periods_options], value=T_AXIS / 3)
n_periods = round(T_AXIS / period)
amplitude = st.sidebar.slider("Amplitude A", min_value=0.0, max_value=2.0, value=1.0, step=0.25)
phase = st.sidebar.slider("Phase initiale φ (rad)", min_value=-np.pi, max_value=np.pi, value=0.0, step=np.pi / 4)

if "running" not in st.session_state:
    st.session_state.running = True
if "t_elapsed" not in st.session_state:
    st.session_state.t_elapsed = 0.0

frequency = 1 / period
omega = 2 * np.pi * frequency

if st.button("⏸️ Pause" if st.session_state.running else "▶️ Reprendre"):
    st.session_state.running = not st.session_state.running

col_period, col_freq, col_omega = st.columns(3)
col_period.metric("Période T", f"{period:.2f} s")
col_freq.metric("Fréquence f", f"{frequency:.2f} Hz")
col_omega.metric("Pulsation ω", f"{omega:.2f} rad/s")

t = np.linspace(0, T_AXIS, 400)
x_marks = np.arange(n_periods + 1) * period  # instants séparés d'exactement une période
labels = [f"$M_{{{i}}}$" for i in range(len(x_marks))]

fig, ax = plt.subplots()
ax.set_xlim(0, T_AXIS)
ax.set_ylim(-Y_LIM, Y_LIM)

# Repère façon "axes mathématiques" : abscisse au milieu, ordonnée sur le bord gauche, flèches aux extrémités
ax.spines["bottom"].set_position(("data", 0))
ax.spines["left"].set_position(("data", 0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize=8)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize=8)
ax.text(1.0, 0.06, "t", transform=ax.get_yaxis_transform(), horizontalalignment="right")
ax.text(0.03, 1.0, "y", transform=ax.get_xaxis_transform(), verticalalignment="top")

for _x in x_marks:
    ax.axvline(_x, linestyle="dashed", c="r", lw=0.8)

(line,) = ax.plot(t, amplitude * np.cos(2 * np.pi * t / period + phase))
scatter = ax.scatter(x_marks, np.zeros_like(x_marks), marker="+", c="r", zorder=5)
texts = [ax.text(_x, 0, label, color="r", horizontalalignment="left") for _x, label in zip(x_marks, labels)]
time_text = ax.text(0.98, 0.95, "", transform=ax.transAxes, horizontalalignment="right", color="gray")

# Cadran cyclique séparé, avec aspect fixé à 1 pour rester circulaire quelle que soit la taille du graphe principal
ax_clock = fig.add_axes((0.78, 0.78, 0.12, 0.12))
ax_clock.set_aspect("equal")
ax_clock.axis("off")
circle_theta = np.linspace(0, 2 * np.pi, 100)
ax_clock.plot(np.cos(circle_theta), np.sin(circle_theta), c="k", lw=1)
(hand,) = ax_clock.plot([0, 0], [0, 0], c="k")
ax_clock.set_xlim(-1.2, 1.2)
ax_clock.set_ylim(-1.2, 1.2)

st_plt = st.pyplot(fig)


def render(t_elapsed):
    # décale la phase avec le temps réel écoulé pour animer le défilement de l'onde
    phase_now = phase - 2 * np.pi * t_elapsed / period
    line.set_ydata(amplitude * np.cos(2 * np.pi * t / period + phase_now))

    # les M_i sont séparés d'une période : ils partagent donc tous la même valeur à un instant donné
    y_mark = amplitude * np.cos(phase_now)
    scatter.set_offsets(np.column_stack([x_marks, np.full_like(x_marks, y_mark)]))
    for txt, _x in zip(texts, x_marks):
        txt.set_position((_x, y_mark))

    frac = (t_elapsed / period) % 1.0
    time_text.set_text(f"t = {frac:.2f} T")

    angle = np.pi / 2 - phase_now
    hand.set_data([0, np.cos(angle)], [0, np.sin(angle)])

    st_plt.pyplot(fig)


if st.session_state.running:
    while st.session_state.running:
        st.session_state.t_elapsed += 0.05
        render(st.session_state.t_elapsed)
        time.sleep(0.05)
else:
    render(st.session_state.t_elapsed)
