from federatedscope.db.processor.basic_processor import BasicSQLProcessor
from federatedscope.db.model.backup import SQLQuery
from federatedscope.db.data.data import DataSet


import xxhash
import random
import math
from sys import maxsize
import numpy as np


class ExternalSQLProcessor(BasicSQLProcessor):
    def __init__(self):
        """

        Args:
            epsilon:
            local_processor:
        """
        # TODO:
        self.epsilon = None
        self.g = 0 # int(round(math.exp(epsilon))) + 1
        self.local_processor = None # local_processor
        # equivalent replacement of OLH bound
        # if < g / (e^\epsilon + g - 1) -> return a random value from [0, g - 1]
        # else -> return true value
        # self.p = float(self.g) / (math.exp(self.epsilon) + self.g - 1)

    def query(self, query: SQLQuery):
        local_result = self.local_processor.query(query)
        perturbed_result = self.lho_perturb(
            local_result, random.randint(0, maxsize))
        return perturbed_result

    def lho_perturb(self, dataset: DataSet, seed):
        for i in range(len(dataset.rows)):
            for j in range(len(dataset.rows[i])):
                h = (xxhash.xxh32(
                    str(dataset.rows[i][j]), seed=seed).intdigest() % self.g)
                threshold = np.random.random_sample()
                if threshold < self.p:
                    dataset.rows[i][j] = random.randint(0, self.g)
                else:
                    dataset.rows[i][j] = h
        return dataset
