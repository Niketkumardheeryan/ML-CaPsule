# This approach comes from SMOTE: Synthetic Minority Over-sampling Technique
# by N. V. Chawla, K. W. Bowyer, L. O. Hall and W. P. Kegelmeyer. To read the
# paper, please go to: https://arxiv.org/pdf/1106.1813.pdf

from sklearn.neighbors import NearestNeighbors
import random


class Smote:
    """
    Implement SMOTE, synthetic minority oversampling technique.

    Parameters
    -----------
    sample      2D (numpy)array
                minority class samples

    N           Integer
                amount of SMOTE N%

    k           Integer
                number of nearest neighbors k
                k <= number of minority class samples

    Attributes
    ----------
    newIndex    Integer
                keep a count of number of synthetic samples
                initialize as 0

    synthetic   2D array
                array for synthetic samples

    neighbors   K-Nearest Neighbors model

    """
    def __init__(self, sample, N, k):
        self.sample = sample
        self.k = k
        self.T = len(self.sample)
        self.N = N
        self.newIndex = 0
        self.synthetic = []
        self.neighbors = NearestNeighbors(n_neighbors=self.k).fit(self.sample)

    def over_sampling(self):
        if self.N < 100:
            self.T = (self.N / 100) * self.T
            self.N = 100
        self.N = int(self.N / 100)

        for i in range(0, self.T):
            nn_array = self.compute_k_nearest(i)
            self.populate(self.N, i, nn_array)

    def compute_k_nearest(self, i):
        nn_array = self.neighbors.kneighbors([self.sample[i]], self.k, return_distance=False)
        if len(nn_array) is 1:
            return nn_array[0]
        else:
            return []

    def populate(self, N, i, nn_array):
        while N is not 0:
            nn = random.randint(0, self.k - 1)
            self.synthetic.append([])
            for attr in range(0, len(self.sample[i])):
                dif = self.sample[nn_array[nn]][attr] - self.sample[i][attr]
                gap = random.random()
                self.synthetic[self.newIndex].append(self.sample[i][attr] + gap * dif)
            self.newIndex += 1
            N -= 1
