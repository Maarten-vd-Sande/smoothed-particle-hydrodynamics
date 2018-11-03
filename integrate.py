from boundary import apply_bound


def euler_step(xy, vel, force, rho, dt, xlim, ylim, damp, hashmap):
    """
    simple euler integration, then apply boundaries
    """
    for i in range(xy.shape[0]):
        vel[i] += dt * force[i] / rho[i]
        xy[i] += dt * vel[i]
        apply_bound(xy, vel, xlim, ylim, damp, i)
        hashmap.move(i, xy[i])
