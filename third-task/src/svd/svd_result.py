from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class SVDResult:

    def __init__(self, u, s, v):
        self.u = u
        self.s = s
        self.v = v

    def apply_k(self, k):
        self.u = self.u[:, :k]
        self.s = self.s[:k]
        self.v = self.v[:k, :]