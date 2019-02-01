import pytest
import numpy as np
from ..data import load_data


def test_cube():
    p = load_data('cube')

    # Check points
    a = [[-0.5, -0.5, 0.5],
         [0.5, -0.5, 0.5],
         [-0.5, 0.5, 0.5],
         [0.5, 0.5, 0.5],
         [-0.5, 0.5, -0.5],
         [0.5, 0.5, -0.5],
         [-0.5, -0.5, -0.5],
         [0.5, -0.5, -0.5]]

    a = np.array(a, dtype='float')
    b = p.points

    assert pytest.approx(a) == b

    # Check faces
    a = ((0, 1, 3, 2),
         (2, 3, 5, 4),
         (4, 5, 7, 6),
         (6, 7, 1, 0),
         (1, 7, 5, 3),
         (6, 0, 2, 4))

    b = tuple(map(tuple, p.faces))

    assert a == b


def test_plot():
    p = load_data('toilet')
    p.plot(symbols=dict(points='r.', edges=None))
