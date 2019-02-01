import os
from ..parser import OffParser

__all__ = ['load_data']


DATA_FOLDER = os.path.abspath(os.path.dirname(__file__))


def load_data(name):
    """
    Loads the built-in data file into an :class:`.OffParser` object.

    Parameters
    ----------
    name : str
        The name of the built-in data file. If the string does not include
        the `.off` file extension, it will be added.
    """
    if not name.endswith('.off'):
        name = '{}.off'.format(name)

    path = os.path.join(DATA_FOLDER, name)

    return OffParser(path)
