import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

__all__ = ['OffParser']


class OffParser():
    """
    An object for parsing and storing data from OFF (Object File Format)
    files, which store 3D model data. See `wikipedia <https://en.wikipedia.org/wiki/OFF_(file_format)>`_
    for the file format specification.

    Parameters
    ----------
    path : str
        The path to the ASCII .OFF file.
    label : str
        The data label.

    Attributes
    ----------
    label : str
        The data label.
    points : array
        The array of vertex points of shape (N, 3).
    faces : list
        A list of lists of point indices constructing each face.
    """
    def __init__(self, path, label=None):
        self.label = label

        if path is not None:
            self.load_ascii(path)

    def __repr__(self):
        return '{}(label={!r}, num_points={!r}, num_faces={!r})'.format(
            type(self).__name__, self.label, len(self.points), len(self.faces))

    @classmethod
    def from_data(cls, data, label=None):
        """
        Creates a new object from parsed data.

        Parameters
        ----------
        data : list
            A list of data.
        label : str
            The data label.
        """
        obj = cls(path=None, label=label)
        obj.load_list(data)
        return obj

    def load_ascii(self, path):
        """
        Loads an ASCII .OFF file into the object.

        Parameters
        ----------
        path : str
            The path to the .OFF file.
        """
        with open(path, 'rt') as fh:
            data = csv.reader(fh, delimiter=' ')
            data = list(data)

        self.load_list(data)

    def load_list(self, data):
        """
        Loads a list of file data into the object.

        Parameters
        ----------
        data : list
            A list of loaded file data.
        """
        # First row should contain OFF
        if len(data[0]) != 1 and data[0][0] != 'OFF':
            raise ValueError('Data does not include OFF header.')

        # Second row should contain number of points and faces
        p, f = [int(x) for x in data[1][:2]]

        # Rows 2 through p should contain points
        points = [r[:3] for r in data[2:p+2]]

        # Rows p+2 through f+p+2 should contain faces
        faces = []

        for r in data[p+2:f+p+2]:
            n = int(r[0])
            face = [int(x) for x in r[1:n+1]]
            faces.append(face)

        self.points = np.array(points, dtype='float')
        self.faces = faces

    def plot(self, ax=None, symbols={}):
        """
        Plots the model in 3D.

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes`
            The axes to which the plot will be added. If None, a new figure and
            axes will be created.
        symbols : dict
            A dictionary of symbols to use for the plot. The following keys
            may be used:

                * 'points': The point symbols, default is None.
                * 'faces': The face color, default is 'g'.
                * 'edges': The edge color, default is '#006400'.

        Examples
        --------
        .. plot:: ../examples/toilet_ex1.py
        """
        if ax is None:
            mx = self.points.max(axis=0)
            c = 0.5 * (mx + self.points.min(axis=0))
            r = 1.1 * np.max(mx - c)
            xlim, ylim, zlim = np.column_stack([c - r, c + r])

            fig = plt.figure()
            ax = fig.add_subplot(111,
                projection='3d',
                xlim=xlim,
                ylim=ylim,
                zlim=zlim,
                xlabel='X',
                ylabel='Y',
                zlabel='Z',
                aspect='equal'
            )

        sym = dict(
            points=None,
            faces='g',
            edges='#006400'
        )
        sym.update(symbols)

        if sym['points'] is not None:
            x = self.points
            ax.plot(x[:,0], x[:,1], x[:,2], sym['points'])

        if sym['faces'] is not None:
            if sym['edges'] is None:
                sym['edges'] = sym['faces']

            v = [self.points[f] for f in self.faces]
            poly = Poly3DCollection(v, edgecolor=sym['edges'], facecolor=sym['faces'])
            ax.add_collection(poly)

        return ax
