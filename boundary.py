def apply_bound(xy, vel, xlim, ylim, damp, i):
    """
    Particles leaving the boundary are placed on the boundary, and 'bounce' backwards.
    """
    if xy[i, 0] < xlim[0]:
        vel[i, 0] *= damp
        xy[i, 0] = xlim[0]
    elif xy[i, 0] > xlim[1]:
        vel[i, 0] *= damp
        xy[i, 0] = xlim[1]

    if xy[i, 1] < ylim[0]:
        vel[i, 1] *= damp
        xy[i, 1] = ylim[0]
    elif xy[i, 1] > ylim[1]:
        vel[i, 1] *= damp
        xy[i, 1] = ylim[1]
