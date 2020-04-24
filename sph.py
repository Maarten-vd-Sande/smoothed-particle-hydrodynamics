import numpy as np
from force import compute_force
from pressure import compute_density_pressure
from integrate import euler_step
import matplotlib.pyplot as plt
from spatialhash import SpatialHash
from matplotlib import animation


# set the base params
n = 1000
width = 400
height = 400
edge = 5
xlim = [edge, width - edge]
ylim = [edge, height - edge]


# set the particle params
mass = 1
k = 20
density = 1
h = 5
visc = 1
f_cons = np.array([0, -0.1])
dt = 0.01
damp = -0.5

# make vectors to store values
xy = np.zeros((n, 2))
vel = np.zeros((n, 2))
force = np.zeros((n, 2))
rho = np.zeros(n)
pre = np.zeros(n)
hashmap = SpatialHash(width, height, h)

# set-up a dam-break scenario
i = 0
dam_ylim = (ylim[0], ylim[1] - 1)
dam_xlim = (int((xlim[1] - xlim[0]) * 0.3), int((xlim[1] - xlim[0]) * 0.8))
if n > ((dam_ylim[1] - dam_ylim[0]) // h) * ((dam_xlim[1] - dam_xlim[0]) // h):
    raise ValueError("reduce the number of points (n) or reduce the kernel radius (h)")

for y in range(*dam_ylim, h):
    for x in range(*dam_xlim, h):
        if i < n:
            xy[i] = x + np.random.uniform(0, h * 0.1), y + np.random.uniform(0, h * 0.1)
            hashmap.move(i, xy[i])
        i += 1
    pass


def animate(i, xy, vel, force, rho, pre, h, mass, k, density, f_cons, dt, visc):
    pre, rho = compute_density_pressure(xy, pre, rho, h, mass, k, density, hashmap)
    force = compute_force(xy, vel, pre, rho, h, mass, visc, f_cons, force, hashmap)
    euler_step(xy, vel, force, rho, dt, xlim, ylim, damp, hashmap)
    scat.set_offsets(xy)



# make an animation
fig = plt.figure()
ax = plt.axes(xlim=(0, width), ylim=(0, height))
scat = ax.scatter([], [])

anim = animation.FuncAnimation(fig, animate, frames=range(5000), interval=1000/60, blit=False, repeat=False,
                               fargs=(xy, vel, force, rho, pre, h, mass, k, density, f_cons, dt, visc))
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim.save('test.mp4')
plt.show()
