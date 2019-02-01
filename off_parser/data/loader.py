import os
import zipfile
import tempfile
import numpy as np
from ..parser import OffParser

try:
    from urllib.request import urlretrieve
except:
    from urllib import urlretrieve

__all__ = [
    'load_data',
    'download_dataset',
    'load_modelnet10',
    'load_modelnet40'
]


DATA_FOLDER = os.path.abspath(os.path.dirname(__file__))


DATASETS = {
    'modelnet10': 'http://3dvision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip',
    'modelnet40': 'http://modelnet.cs.princeton.edu/ModelNet40.zip'
}


def load_data(name):
    """
    Loads the built-in data file into an :class:`.OffParser` object.

    Parameters
    ----------
    name : str
        The name of the built-in data file. If the string does not include
        the `.off` file extension, it will be added. The following names are
        available:

            * 'cube'
            * 'toilet'
    """
    if not name.endswith('.off'):
        name = '{}.off'.format(name)

    path = os.path.join(DATA_FOLDER, name)

    return OffParser(path)


def download_dataset(name):
    """
    Downloads the named dataset to the system temporary folder.

    Parameters
    ----------
    name : str
        The name of the dataset. The following names are available:

            * 'modelnet10'
            * 'modelnet40'
    """
    url = DATASETS[name]
    fname = url.split('/')[-1]
    dirname = tempfile.gettempdir()
    path = os.path.join(dirname, fname)

    if not os.path.isfile(path):
        urlretrieve(url, path)

    return path


def _load_modelnet(name, partition):
    """
    Downloads the specified modelnet datasets and yields generated elements.

    Parameters
    ----------
    name : str
        The name of the dataset.
    partition : {'train', 'test'}
        The dataset partition to load.
    """
    path = download_dataset(name)
    s = '/{}/'.format(partition)

    with zipfile.ZipFile(path, 'r') as fh:
        for name in fh.namelist():
            if name.endswith('.off') and not name.startswith('__MACOSX') and s in name:
                data = fh.read(name)
                data = data.decode('utf-8')
                data = data.split('\n')
                data = [x.split(' ') for x in data]
                data = OffParser.from_data(data)
                data.label = name.split('/')[-3]

                yield data


def load_modelnet10(partition):
    """
    Downloads the ModelNet10 dataset and returns a generator of
    :class:`.OffParser` objects. The dataset is described
    `here <http://modelnet.cs.princeton.edu/>`_.

    Parameters
    ----------
    partition : {'train', 'test'}
        The dataset partition to load.
    """
    return _load_modelnet('modelnet10', partition)


def load_modelnet40(partition):
    """
    Downloads the ModelNet40 dataset and returns a generator of
    :class:`.OffParser` objects. The dataset is described
    `here <http://modelnet.cs.princeton.edu/>`_.

    Parameters
    ----------
    partition : {'train', 'test'}
        The dataset partition to load.
    """
    return _load_modelnet('modelnet40', partition)
