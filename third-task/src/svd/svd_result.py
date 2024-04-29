from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class SVDResult:

    def __init__(self, u, s, v, k):
        self.u = u[:, :k]
        self.s = s[:k]
        self.v = v[:k, :]
