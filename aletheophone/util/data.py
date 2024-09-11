from numpy import array, ndarray
from struct import unpack
from typing import List


def deserialize_float32(data: bytes) -> ndarray:
    num_floats = len(data) // 4
    return array(list(unpack("%sf" % num_floats, data)))
