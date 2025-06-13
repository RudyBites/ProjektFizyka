import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import random

# Stałe
G = 6.674e-11
M = 5.972e24
R = 6.371e6
dt = 1
height = 900000
max_steps = 5000

# Wykres
fig, ax = plt.subplots(figsize=(12, 12))
plt.subplots_adjust(bottom=0.3)
ax.set_xlim(-10.5e6, 10.5e6)
ax.set_ylim(-10.5e6, 10.5e6)
ax.set_aspect('equal', 'box')
ax.set_title("Symulacja działa Newtona – pocisk w ruchu")
ax.set_xticks([])
ax.set_yticks([])

# Ziemia
earth = plt.Circle((0, 0), R, color='green', alpha=0.5)
ax.add_artist(earth)

# Góra i armata
mountain_width = 6e5
peak = [0, R + height]
mountain_x = [-mountain_width / 2, 0, mountain_width / 2]
mountain_y = [R, R + height, R]
ax.plot(mountain_x, mountain_y, color='brown', linewidth=2)
ax.plot([peak[0]], [peak[1]], 'r^')
armata_label = ax.text(
    0, ax.get_ylim()[1] - 2e5,
    'Armata na czubku góry',
    color='red', fontsize=11,
    ha='center', va='top',
)

# Suwaki
ax_slider_v0 = plt.axes([0.25, 0.1, 0.6, 0.03])
slider_v0 = Slider(ax_slider_v0, 'Prędkość v₀ [m/s]', 1000, 12000, valinit=7400, valstep=100)

ax_slider_angle = plt.axes([0.25, 0.15, 0.6, 0.03])
slider_angle = Slider(ax_slider_angle, 'Kąt wystrzału [°]', 0, 90, valinit=0, valstep=1)

ax_button_fire = plt.axes([0.3, 0.02, 0.1, 0.04])
button_fire = Button(ax_button_fire, 'Fire!')

ax_button_clear = plt.axes([0.6, 0.02, 0.1, 0.04])
button_clear = Button(ax_button_clear, 'Clear')

# Globalne
all_static_lines = []
active_point = [None]
active_anim = [None]


def fire(event):
    v0 = slider_v0.val
    angle_deg = slider_angle.val
    angle_rad = np.radians(angle_deg)

    vel = np.array([
        v0 * np.cos(angle_rad),
        v0 * np.sin(angle_rad)
    ])
    pos = np.array([0.0, R + height])
    traj_x = [pos[0]]
    traj_y = [pos[1]]

    if active_point[0]:
        active_point[0].remove()
    point_dot, = ax.plot([], [], 'ro', markersize=4)
    active_point[0] = point_dot

    color = random.choice(['red', 'green', 'blue', 'orange', 'purple', 'magenta', 'cyan'])
    static_line, = ax.plot([], [], color=color, linewidth=1)
    all_static_lines.append(static_line)

    def update(frame):
        nonlocal pos, vel, traj_x, traj_y

        for _ in range(5):
            r = np.linalg.norm(pos)
            if r < R:
                ani.event_source.stop()
                point_dot.set_data([], [])
                return point_dot, static_line

            r_hat = -pos / r
            a = G * M / r ** 2 * r_hat
            vel += a * dt
            pos += vel * dt
            traj_x.append(pos[0])
            traj_y.append(pos[1])


            if frame > 100 and np.linalg.norm(pos - np.array([0.0, R + height])) < 1e4:
                ani.event_source.stop()
                point_dot.set_data([], [])
                return point_dot, static_line

        point_dot.set_data([pos[0]], [pos[1]])
        static_line.set_data(traj_x, traj_y)
        return point_dot, static_line

    ani = FuncAnimation(fig, update, frames=range(0, max_steps, 5), interval=5, blit=False)
    active_anim[0] = ani
    plt.draw()


def clear(event):
    if active_point[0]:
        active_point[0].remove()
        active_point[0] = None
    for line in all_static_lines:
        line.remove()
    all_static_lines.clear()
    plt.draw()

# Połączenia
button_fire.on_clicked(fire)
button_clear.on_clicked(clear)

plt.show()
