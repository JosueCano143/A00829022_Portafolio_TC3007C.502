import scipy as sp
import numpy as np


class FDGF():
    def __init__(self, nu=0.99, ws=15, mu=10, sigma=1):
        self.nu = nu
        self.window_size = ws
        self.mu = mu
        self.sigma = sigma

        self.reset()

    def reset(self):
        # Get the time series
        series = np.linspace(
            np.max(self.mu - 3 * self.sigma, 0),
            self.mu + 3 * self.sigma,
            self.window_size
        )

        # Get the integer derivatives
        dG0 = self._df0dt0(series)
        dG1 = self._df1dt1(series)

        # Components
        self.dG0x = np.tile(dG0, (self.window_size, 1))
        nu_int = np.floor(self.nu)
        nu_fra = self.nu - nu_int
        gamma = nu_fra / (1 - nu_fra)

        if nu_int == 0:
            DG = self.cf_gauss_der(series)
        elif nu_int == 1:
            DG = (gamma + 1) * dG1 - gamma * self.cf_gauss_der(series)
        else:
            raise NotImplementedError("Fractional order not implemented")

        self.DG = np.reshape(DG, (DG.shape[0], 1))

    def _df_base(self, var):
        return np.exp(-(self.mu - var) ** 2 / (2 * self.sigma ** 2))

    def _df0dt0(self, var):
        exp_fun = self._df_base(var)
        scale_constant = self.sigma * np.sqrt(2 * np.pi)
        return exp_fun / scale_constant

    def _df1dt1(self, var):
        exp_fun = self._df_base(var) * 2 * (self.mu - var)
        scale_constant = 2 * (self.sigma ** 3) * np.sqrt(2 * np.pi)
        return exp_fun / scale_constant

    def _int_func(self, x, a1, t1):
        sigma2 = self.sigma ** 2
        return np.exp(
            -(x * x - 2 * x * (self.mu + sigma2 * a1)
              + self.mu ** 2 + 2 * sigma2 * a1 * t1) / (2 * sigma2))

    def cf_gauss_der(self, var):
        alpha = self.nu / (1 - self.nu)
        par1 = -(var - self.mu - (self.sigma ** 2) * alpha / 2) * alpha
        par3 = (self.mu / self.sigma + self.sigma * alpha) / np.sqrt(2)
        par2 = var / (self.sigma * np.sqrt(2)) - par3

        y = []
        for v in var:
            y.append(sp.integrate.quadrature(
                lambda x: self._int_func(x, alpha, v), 0, v)[0])

        ks = np.sqrt(1 / (2 * np.pi)) * (1 + alpha) / self.sigma
        Df1 = np.exp(par1 - par2 ** 2) - np.exp(par1 - par3 ** 2)
        Df2 = alpha * np.array(y)
        return ks * (Df1 - Df2)


if __name__ == "__main__":
    fdgf = FDGF()
    print(fdgf.DG)
