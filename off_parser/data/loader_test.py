from .loader import *


def test_load_modelnet10():
    p = load_modelnet10('train')
    next(p)
    p = load_modelnet10('test')
    next(p)


def test_load_modelnet40():
    p = load_modelnet40('train')
    next(p)
    p = load_modelnet40('test')
    next(p)
