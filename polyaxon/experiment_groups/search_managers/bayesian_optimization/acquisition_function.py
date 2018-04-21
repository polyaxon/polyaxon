from scipy.stats import norm


class AcquisitionFunction(object):
    """The acquisition / utility function.

    Params:
        fct: `str`, The supported functions are:
            * ucb: GP Upper Confidence Bound
            * ei: Expected Improvement
            * poi: Probability of Improvement
        kappa: `float`, a tunable parameter of GP Upper Confidence Bound, to balance exploitation
                against exploration, increasing kappa will make the optimized hyperparameters
                pursuing exploration.
    """
    UCB = 'ucb'
    EI = 'ei'
    POI = 'poi'
    FUNCTIONS = {UCB, EI, POI}

    def __init__(self, fct, gaussian_process, kappa=None, xi=None):
        """
        If UCB is to be used, a constant kappa is needed.
        """
        if fct not in self.FUNCTIONS:
            raise ValueError('the acquisition function `{}` is not supported. '
                             'Supported values are `{}`.'.format(fct, self.FUNCTIONS))

        if fct == self.UCB and kappa is None:
            raise ValueError('the acquisition function `ucb` requires a parameter `kappa`')

        if fct in {self.EI, self.POI} and xi is None:
            raise ValueError('the acquisition function `{}` requires a parameter `xi`'.format(
                self.fct
            ))

        self.fct = fct
        self.gaussian_process = gaussian_process
        self.kappa = kappa
        self.xi = xi

    def compute(self, x, y_max):
        if self.fct == self.UCB:
            return self.compute_ucb(x=x,
                                    gaussian_process=self.gaussian_process,
                                    kappa=self.kappa)
        if self.fct == self.EI:
            return self.compute_ei(x=x,
                                   gaussian_process=self.gaussian_process,
                                   y_max=y_max,
                                   xi=self.xi)
        if self.fct == self.POI:
            return self.compute_poi(x=x,
                                    gaussian_process=self.gaussian_process,
                                    y_max=y_max,
                                    xi=self.xi)

    @staticmethod
    def compute_ucb(x, gaussian_process, kappa):
        mean, std = gaussian_process.predict(x, return_std=True)
        return mean + kappa * std

    @staticmethod
    def compute_ei(x, gaussian_process, y_max, xi):
        mean, std = gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - xi)/std
        return (mean - y_max - xi) * norm.cdf(z) + std * norm.pdf(z)

    @staticmethod
    def compute_poi(x, gaussian_process, y_max, xi):
        mean, std = gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - xi)/std
        return norm.cdf(z)
