#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from scipy.optimize import minimize
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern

from polyaxon.polyflow import (
    AcquisitionFunctions,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
)
from polyaxon.polytune.search_managers.utils import get_random_generator


class UtilityFunction:
    def __init__(self, config, seed=None):
        if not isinstance(config, UtilityFunctionConfig):
            raise ValueError("Received a non valid configuration.")

        self.config = config
        self.eps = config.eps
        self.kappa = config.kappa
        self.acquisition_function = config.acquisition_function
        self.random_generator = get_random_generator(seed=seed)
        self.gaussian_process = self.get_gaussian_process(
            config=config.gaussian_process, random_generator=self.random_generator
        )

    @staticmethod
    def get_gaussian_process(config, random_generator):
        if not isinstance(config, GaussianProcessConfig):
            raise ValueError("Received a non valid configuration.")

        if GaussianProcessesKernels.is_rbf(config.kernel):
            kernel = RBF(length_scale=config.length_scale)
        else:
            kernel = Matern(length_scale=config.length_scale, nu=config.nu)

        return GaussianProcessRegressor(
            kernel=kernel,
            n_restarts_optimizer=config.num_restarts_optimizer,
            random_state=random_generator,
        )

    def _compute_ucb(self, x):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        return mean + self.kappa * std

    def _compute_ei(self, x, y_max):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - self.eps) / std
        return (mean - y_max - self.eps) * norm.cdf(z) + std * norm.pdf(z)

    def _compute_poi(self, x, y_max):
        mean, std = self.gaussian_process.predict(x, return_std=True)
        z = (mean - y_max - self.eps) / std
        return norm.cdf(z)

    def compute(self, x, y_max):
        if AcquisitionFunctions.is_ucb(self.acquisition_function):
            return self._compute_ucb(x=x)
        if AcquisitionFunctions.is_ei(self.acquisition_function):
            return self._compute_ei(x=x, y_max=y_max)
        if AcquisitionFunctions.is_poi(self.acquisition_function):
            return self._compute_poi(x=x, y_max=y_max)

    def max_compute(self, y_max, bounds, num_warmup=100000, num_iterations=250):
        """A function to find the maximum of the acquisition function

        It uses a combination of random sampling (cheap) and the 'L-BFGS-B' optimization method.

        First by sampling `num_warmup` (1e5) points at random,
        and then running L-BFGS-B from `num_iterations` (250) random starting points.

        Params:
            y_max: The current maximum known value of the target function.
            bounds: The variables bounds to limit the search of the acq max.
            num_warmup: The number of times to randomly sample the acquisition function
            num_iterations: The number of times to run scipy.minimize

        Returns
            x_max: The arg max of the acquisition function.
        """
        # Warm up with random points
        x_tries = self.random_generator.uniform(
            bounds[:, 0], bounds[:, 1], size=(num_warmup, bounds.shape[0])
        )
        ys = self.compute(x_tries, y_max=y_max)
        x_max = x_tries[ys.argmax()]
        max_acq = ys.max()

        # Explore the parameter space more throughly
        x_seeds = self.random_generator.uniform(
            bounds[:, 0], bounds[:, 1], size=(num_iterations, bounds.shape[0])
        )
        for x_try in x_seeds:
            # Find the minimum of minus the acquisition function
            res = minimize(
                lambda x: -self.compute(x.reshape(1, -1), y_max=y_max),
                x_try.reshape(1, -1),
                bounds=bounds,
                method="L-BFGS-B",
            )

            # See if success
            if not res.success:
                continue

            # Store it if better than previous minimum(maximum).
            if max_acq is None or -res.fun[0] >= max_acq:
                x_max = res.x
                max_acq = -res.fun[0]

        # Clip output to make sure it lies within the bounds. Due to floating
        # point technicalities this is not always the case.
        return np.clip(x_max, bounds[:, 0], bounds[:, 1])
