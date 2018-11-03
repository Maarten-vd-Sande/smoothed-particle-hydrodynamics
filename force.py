import numpy as np
from math import sqrt, pi


def compute_force(xy, vel, pre, rho, h, mass, visc, f_cons, force, hashmap):
    """
    calculate the force of the pressure and viscosity
    """
    # pre-calculate some part of kernels
    h_6 = h ** 6
    pre_spiky = mass * -45 / (pi * h_6)
    pre_lapla = visc * mass * 45 / (pi * h_6)

    for i in range(xy.shape[0]):
        # pressure force
        f_pres = np.array([0, 0], dtype=float)
        # viscosity force
        f_visc = np.array([0, 0], dtype=float)

        for j in hashmap.neighbours(xy[i]):
            if i == j:
                continue

            r = xy[j] - xy[i]
            n = sqrt(r.dot(r))

            if 0 < n < h:
                f_pres += -r / n * (pre[i] + pre[j]) / (2 * rho[j]) * pre_spiky * ((h - n) ** 2)

                f_visc += visc * mass * (vel[j] - vel[i]) / rho[j] * pre_lapla * (h - n)

        force[i] = f_pres + f_visc + f_cons
    return force
