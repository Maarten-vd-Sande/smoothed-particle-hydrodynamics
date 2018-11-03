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
xlim = [40, width - 40]
ylim = [40, height - 40]

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
for y in range(ylim[0], ylim[1]-100, h):
    for x in range(xlim[0] + 100, xlim[1]-50, h):
        if i < n:
            xy[i] = x + np.random.normal(0, 0.25), y + np.random.normal(0, 0.25)
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
