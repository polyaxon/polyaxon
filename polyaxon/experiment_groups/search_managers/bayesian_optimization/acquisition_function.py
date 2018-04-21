from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern

from experiment_groups.search_managers.utils import get_random_generator
from polyaxon_schemas.settings import GaussianProcessConfig, UtilityFunctionConfig
from polyaxon_schemas.utils import AcquisitionFunctions, GaussianProcessesKernels


class UtilityFunction(object):
    UCB = 'ucb'
    EI = 'ei'
    POI = 'poi'
    FUNCTIONS = {UCB, EI, POI}

    def __init__(self, config, seed=None):
        if not isinstance(config, UtilityFunctionConfig):
            raise ValueError('Received a non valid configuration.')

        self.config = config
        self.xi = config.xi
        self.kappa = config.kappa
        self.acquisition_function = config.acquisition_function
        self.gaussian_process = self.get_gaussian_process(config=config.gaussian_process, seed=seed)

    @staticmethod
    def get_gaussian_process(config, seed=None):
        if not isinstance(config, GaussianProcessConfig):
            raise ValueError('Received a non valid configuration.')

        random_generator = get_random_generator(seed=seed)

        if GaussianProcessesKernels.is_rbf(config.kernel):
            kernel = RBF(length_scale=config.length_scale)
        else:
            kernel = Matern(length_scale=config.length_scale,
                            nu=config.nu)

        return GaussianProcessRegressor(
            kernel=kernel,
            n_restarts_optimizer=config.n_restarts_optimizer,
            random_state=random_generator
        )

    def compute(self, x, y_max):
        if AcquisitionFunctions.is_ucb(self.acquisition_function):
            return self.compute_ucb(x=x)
        if AcquisitionFunctions.is_ei(self.acquisition_function):
            return self.compute_ei(x=x, y_max=y_max)
        if AcquisitionFunctions.is_poi(self.acquisition_function):
            return self.compute_poi(x=x, y_max=y_max)

    def compute_ucb(self, x):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        return mean + self.kappa * std

    def compute_ei(self, x, y_max):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - self.xi) / std
        return (mean - y_max - self.xi) * norm.cdf(z) + std * norm.pdf(z)

    def compute_poi(self, x, y_max):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - self.xi) / std
        return norm.cdf(z)
