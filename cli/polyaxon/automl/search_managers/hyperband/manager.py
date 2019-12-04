import math

from polyaxon.automl.search_managers.base import BaseManager
from polyaxon.automl.search_managers.random_search.manager import RandomSearchManager
from polyaxon.schemas.polyflow.parallel import HyperbandConfig, RandomSearchConfig


class HyperbandManager(BaseManager):
    """Hyperband search strategy manager for hyperparameter optimization.

    The strategy runs in the following way:

    def run(self):
        results = []

        for bracket in reversed(range(self.s_max)):
            n_runs = self.get_n_runs(bracket=bracket)
            n_resources = self.get_resources(bracket=bracket)

            suggestions = [get_suggestions(...) for _ in range(n_runs)]

            for bracket_iteration in range(bracket + 1):
                n_runs_to_keep = self.get_n_run_to_keep(
                    n_runs=n_runs, bracket_iteration=bracket_iteration)
                n_iterations = self.get_n_resources(
                    n_resources=n_resources, bracket_iteration=bracket_iteration)

                val_losses = []
                early_stops = []

                for suggestion in suggestions:
                    result = run_suggestions(n_iterations, suggestion)
                    loss = result['loss']
                    val_losses.append(loss)
                    early_stop = result.get('early_stop', False)
                    early_stops.append(early_stop)
                    results.append(result)

                # select a number of best configurations for the next loop
                # filter out early stops, if any
                indices = np.argsort(val_losses)
                suggestions = [suggestions[i] for i in indices if not early_stops[i]]
                suggestions = suggestions[:n_runs_to_keep]

        return results
    """

    CONFIG = HyperbandConfig

    def __init__(self, config):
        self.config = config
        # Maximum iterations per configuration
        self.max_iter = config.max_iter
        # Defines configuration downsampling/elimination rate (default = 3)
        self.eta = config.eta
        # number of times to run hyperband (brackets)
        self.s_max = int(math.log(self.max_iter) / math.log(self.eta))
        # i.e.  # of times to repeat the outer loops over the tradeoffs `s`
        self.B = (
            self.s_max + 1
        ) * self.max_iter  # budget per bracket of successive halving

    def get_bracket(self, iteration):
        """This defines the bracket `s` in outerloop `for s in reversed(range(self.s_max))`."""
        return self.s_max - iteration

    def get_n_runs(self, bracket):
        # n: initial number of configs
        return int(
            math.ceil((self.B / self.max_iter) * (self.eta ** bracket) / (bracket + 1))
        )

    def get_resources(self, bracket):
        # r: initial number of iterations/resources per config
        return self.max_iter * (self.eta ** (-bracket))

    def get_resources_for_iteration(self, iteration):
        bracket = self.get_bracket(iteration=iteration)
        return self.get_resources(bracket=bracket)

    def get_n_runs_to_keep(self, n_runs, bracket_iteration):
        """Return the number of configs to keep and resume."""
        n_runs = n_runs * (self.eta ** -bracket_iteration)
        return int(n_runs / self.eta)

    def get_n_runs_to_keep_for_iteration(self, iteration, bracket_iteration):
        """Return the number of configs to keep for an iteration and iteration bracket.

        This is just util function around `get_n_runs_to_keep`
        """
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration == bracket + 1:
            # End of loop `for bracket_iteration in range(bracket + 1):`
            return 0

        n_runs = self.get_n_runs(bracket=bracket)
        return self.get_n_runs_to_keep(
            n_runs=n_runs, bracket_iteration=bracket_iteration
        )

    def get_n_resources(self, n_resources, bracket_iteration):
        """Return the number of iterations to run for this barcket_i"""
        return n_resources * self.eta ** bracket_iteration

    def get_n_resources_for_iteration(self, iteration, bracket_iteration):
        """Return the number of iterations to run for this barcket_i

        This is just util function around `get_n_resources`
        """
        bracket = self.get_bracket(iteration=iteration)
        n_resources = self.get_resources(bracket=bracket)
        return self.get_n_resources(
            n_resources=n_resources, bracket_iteration=bracket_iteration
        )

    def get_suggestions(self, iteration, bracket_iteration):
        """Return a list of suggestions/arms based on hyperband."""
        bracket = self.get_bracket(iteration=iteration)
        n_runs = self.get_n_runs(bracket=bracket)
        n_resources = self.get_n_resources_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        )
        n_resources = self.config.resource.cast_value(n_resources)
        suggestion_params = {self.config.resource.name: n_resources}
        config = RandomSearchConfig(
            matrix=self.config.matrix, n_runs=n_runs, seed=self.config.seed
        )
        return RandomSearchManager(config=config).get_suggestions(
            suggestion_params=suggestion_params
        )

    def should_reschedule(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration < bracket:
            # The bracket is still processing
            return False

        # We can only reschedule if we can create a new bracket
        return self.get_bracket(iteration=iteration + 1) >= 0

    def should_reduce_configs(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another bracket iteration."""
        n_runs_to_keep = self.get_n_runs_to_keep_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        )
        return n_runs_to_keep > 0
