from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from common.utils import draw_angle, arrow_dxdy

min_n = 1.0
max_n = 10.0

cmap = plt.colormaps.get_cmap('Blues')
norm = colors.Normalize(min_n, max_n)

st.set_page_config(page_title="Dioptre Plan", page_icon="📐")

st.title('Dioptre plan')

st.sidebar.header('Dioptre Plan')
st.sidebar.write('Paramètres')

n1 = st.sidebar.slider('n1', min_n, max_n)  # 👈 this is a widget
n2= st.sidebar.slider('n2', min_n, max_n)  # 👈 this is a widget
i1 = st.sidebar.slider('i1', 0, 90, 30)  # 👈 this is a widget

i_lim = np.nan
i2 = np.nan
if n2 < n1:
    i_lim = np.degrees(np.asin(n2/n1))

if (n2 < n1 and i1 < i_lim) or (n2 > n1):
    i2 = np.degrees(np.asin(n1 / n2 * np.sin(np.radians(i1))))

    
radius = np.sqrt(2)
input_ray = [-radius * np.sin(np.radians(i1)), 0], [radius * np.cos(np.radians(i1)), 0]
refracted_ray = [0, radius * np.sin(np.radians(i2))], [0, -radius * np.cos(np.radians(i2))]
reflected_ray = [0, radius * np.sin(np.radians(i1))], [0, radius * np.cos(np.radians(i1))]


limit_ray = [-np.sign(i1+1e-12) * radius * np.sin(np.radians(np.abs(i_lim))), 0], \
    [radius * np.cos(np.radians(i_lim)), 0]


if n1 > n2:
    i_lim_label = r'$\mid \theta_{lim} \mid$ '
    st.write(r'$n_2 < n_1  \Rightarrow\, \mid \theta_{lim} \mid = $' + f'{i_lim:3.2f}°')
else:
    st.write('$n_2 > n_1$')

def draw_arrow(ax, xs, ys, scale=0.05, **kwargs):

    dx, dy = arrow_dxdy(xs, ys, scale=scale)
    x_arrow = np.mean(xs)
    y_arrow = np.mean(ys)
    
    arrow_kwargs =  dict(shape='full', lw=0, length_includes_head=True, head_width=.05)
    arrow_kwargs.update(**kwargs)
    ax.arrow(x_arrow, y_arrow, dx, dy, **arrow_kwargs)
    
    
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.fill_between([-1, 1], 0, 1, color=cmap(norm(n1)), alpha=0.5)
ax.fill_between([-1, 1], -1, 0, color=cmap(norm(n2)), alpha=0.5)
ax.axhline(0, c='k', linewidth=2)
ax.axvline(0, c='k', linewidth=1, linestyle='dashed')
ax.scatter(0,0, s=50, c='k')
ax.plot(*limit_ray, c='k', linestyle='dotted')

ax.text(-0.9, 0.1, '$n_1$', verticalalignment='center',)
ax.text(-0.9, -0.1, '$n_2$', verticalalignment='center',)


# incoming ray
ax.plot(*input_ray, c='r')
draw_arrow(ax, *input_ray, color='r')
draw_angle(ax, i1, color='r')


ax.plot(*refracted_ray, c='g')
draw_arrow(ax, *refracted_ray, color='g')
draw_angle(ax, i2, top=False, color='g')


if not np.isnan(i_lim) and np.abs(i1) >= np.abs(i_lim):
    ax.plot(*reflected_ray, c='r')
    draw_arrow(ax, *reflected_ray, color='r')
    draw_angle(ax, -i1, radius=0.8, color='r')
    
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_axis_off()

st.pyplot(fig)
