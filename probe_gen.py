import numpy as np

from probeinterface import Probe


def set_probe_for(recording, n=61):
    positions = np.zeros((n, 2))
    for i in range(n):
        x = i // 8
        y = i % 8
        positions[i] = x, y
    positions *= 20
    positions[8:16, 1] -= 10

    probe = Probe(ndim=2, si_units='um')
    probe.set_contacts(positions=positions, shapes='circle', shape_params={'radius': 5})

    polygon = [(-20, -30), (20, -110), (60, -30), (60, 190), (-20, 190)]
    probe.set_planar_contour(polygon)
    return recording.set_probe(probe)



if __name__ == '__main__':
    pass