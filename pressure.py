from math import pi

def compute_density_pressure(xy, pre, rho, h, mass, k, density, hashmap):
    """
    calculate the density and pressure of each particle
    """
    # pre-calculate some part of kernel
    h_2 = h ** 2
    h_9 = h ** 9
    pre_poly6 = mass * 315 / (64 * pi * h_9)

    for i in range(xy.shape[0]):
        rho[i] = 0
        for j in hashmap.neighbours(xy[i]):
            r = xy[j] - xy[i]
            r_2 = r.dot(r)

            if r_2 <= h_2:
                rho[i] += pre_poly6 * (h_2 - r_2) ** 3

        pre[i] = k * (rho[i] - density)

    return pre, rho
