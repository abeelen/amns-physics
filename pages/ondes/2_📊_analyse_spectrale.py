import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.title("Analyse Spectrale")

T_TOTAL_MS = 100.0  # durée totale calculée pour la FFT (ms), fixe
N_SAMPLES = 10_000  # nombre d'échantillons temporels, fixe
DUREE_AFFICHEE_MS = 20.0  # fenêtre de temps affichée, fixe
FREQ_MAX_HZ = 5000.0  # échelle du spectre, fixe
N_HARMONIQUES = 5  # nombre de composantes, toujours affichées
AMPLITUDE_MAX = 5  # niveau d'amplitude max par harmonique (0 à 5)

PRESETS = {
    "Onde pure": [5, 0, 0, 0, 0],
    "Deux harmoniques égales": [5, 5, 0, 0, 0],
    "Timbre riche (décroissant)": [5, 3, 2, 1, 1],
}


def apply_preset():
    preset = st.session_state.preset_choice
    if preset == "Bruit (aléatoire)":
        valeurs = np.random.default_rng().integers(0, AMPLITUDE_MAX + 1, size=N_HARMONIQUES)
    else:
        valeurs = PRESETS[preset]
    for i, v in enumerate(valeurs, start=1):
        st.session_state[f"harmonique_{i}"] = int(v)


for i, v in enumerate(PRESETS["Onde pure"], start=1):
    st.session_state.setdefault(f"harmonique_{i}", v)

st.selectbox(
    "Préréglages utiles",
    [*PRESETS, "Bruit (aléatoire)"],
    key="preset_choice",
    on_change=apply_preset,
)

st.sidebar.write("Paramètres")
fondamentale_hz = st.sidebar.select_slider("Fréquence fondamentale (Hz)", options=[220, 440, 880], value=440)
harmoniques = [
    st.sidebar.slider(
        f"Harmonique {i} ({i * fondamentale_hz} Hz)",
        min_value=0,
        max_value=AMPLITUDE_MAX,
        step=1,
        value=st.session_state[
            f"harmonique_{i}"
        ],  # évite la réinitialisation quand le libellé change avec la fréquence
        key=f"harmonique_{i}",
    )
    for i in range(1, N_HARMONIQUES + 1)
]

t_ms = np.linspace(0, T_TOTAL_MS, N_SAMPLES, endpoint=False)
freq_axis = np.fft.rfftfreq(N_SAMPLES, d=np.median(np.diff(t_ms / 1000)))

spectre = np.zeros_like(freq_axis)
for i, amplitude in enumerate(harmoniques, start=1):
    spectre[np.argmin(np.abs(freq_axis - i * fondamentale_hz))] = amplitude

onde = np.fft.irfft(spectre, n=N_SAMPLES)
pic = np.max(np.abs(onde))
if pic > 0:
    onde = onde / pic

fig, (ax_onde, ax_spec) = plt.subplots(ncols=2, figsize=(10, 4))

ax_onde.plot(t_ms, onde, linewidth=2, color="tab:red")
ax_onde.set_xlim(0, DUREE_AFFICHEE_MS)
ax_onde.set_ylim(-1.1, 1.1)
ax_onde.set_xlabel("Temps [ms]")
ax_onde.set_ylabel("Amplitude")
ax_onde.set_title("Signal temporel")

ax_spec.bar(
    fondamentale_hz * np.arange(1, N_HARMONIQUES + 1),
    harmoniques,
    width=fondamentale_hz * 0.15,
    color="tab:red",
)
ax_spec.set_xlim(0, FREQ_MAX_HZ)
ax_spec.set_ylim(0, AMPLITUDE_MAX + 0.5)
ax_spec.set_xlabel("Fréquence [Hz]")
ax_spec.set_ylabel("Amplitude")
ax_spec.set_title("Spectre")

fig.tight_layout()
st.pyplot(fig)
