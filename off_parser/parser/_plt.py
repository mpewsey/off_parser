# This module configures matplotlib

import os
import matplotlib

if 'DISPLAY' not in os.environ:
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__all__ = ['plt']
