import math
import numpy as np
import scipy.linalg as la


class MJLS:
    """A Markov Jump Linear System."""
    def __init__(self, N, A, B, C, D, P=None, X=None, F=None):
        self._N = N
        self._A = A
        self._B = B
        self._C = C
        self._D = D
        self._P = P
        self._X = X
        self._F = F

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, value):
        self._N = value

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, value):
        self._A = value

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, value):
        self._B = value

    @property
    def C(self):
        return self._C

    @C.setter
    def C(self, value):
        self._C = value

    @property
    def D(self):
        return self._D

    @D.setter
    def D(self, value):
        self._D = value

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, value):
        self._P = value

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        self._X = value

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, value):
        self._F = value

    def get_ABCD(self, i=None):
        """Returns :obj: `A`, `B', `C', and `D' matrices.

        Returns all `A''s, `B''s, `C''s and `D''s, or the
        `i'th one, if `i' is provided.

        Args:
            i (:obj:`int`, optional): index used to retrive
                the matrices.
        """
        if(i is not None):
            return (self.A[i], self.B[i], self.C[i], self.D[i])
        else:
            return (self.A, self.B, self.C, self.D)


def test_stability(m, lambd):
    """Tests parameters for TD(\lambda) stability.

    Based on the article:

    O. L. V. Costa and J. C. C. Aya, "Monte Carlo
    TD(\lambda)-methods for the optimal control of
    discrete-time Markovian jump linear systems",
    Automatica, vol. 38, pp. 217–225, 2002.

    Args:
        m (:obj:`MJLS`): the corresponding Markov Jump Linear System.
        lambd (:obj:`float`): the $\lambda$ value to be tested.

    """
    assert m.F is not None, "F must be provided"

    krs = []
    v_max = -math.inf
    for i in range(m.N):
        G = m.A[i] + m.B[i].dot(m.F[i])
        kr = np.kron(G, G)
        krs.append(kr)

        # lambda test
        v = pow(la.norm(kr, ord=2), -1)
        if v > v_max:
            v_max = v

    # Fs test
    I_cal = la.block_diag(*krs)

    if not (max(abs(la.eig(I_cal)[0])) < 1):
        print('test_stability: WARNING: F does not satisfy Lemma 3 '
              '(stabilizability)')

    if not (pow(lambd, 2) < v_max):
        print('test_stability: WARNING: lambda does not satisfy Lemma 2 '
              '(convergence)')
