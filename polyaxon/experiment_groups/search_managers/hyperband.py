import math

from experiment_groups.search_managers.base import BaseSearchAlgorithmManager
from experiment_groups.search_managers.utils import get_random_suggestions


def get_best_config():
    pass


class HyperbandSearchManager(BaseSearchAlgorithmManager):
    """Hyperband search algorithm manager for hyperparameter optimization.

    The algorithm runs in the following way:

    def run(self):
        results = []

        for bracket in reversed(range(self.s_max)):
            n_configs = self.get_number_of_configs(bracket=bracket)
            n_resources = self.get_resources(bracket=bracket)

            suggestions = [get_suggestions(...) for _ in range(n_configs)]

            for bracket_iteration in range(bracket + 1):
                n_configs_to_keep = self.get_n_config_to_keep(
                    n_suggestions=n_configs, bracket_iteration=bracket_iteration)
                n_iterations = self.get_n_iteration(
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
                suggestions = suggestions[:n_configs_to_keep]

        return results
    """

    def __init__(self, params_config):
        super(HyperbandSearchManager, self).__init__(params_config=params_config)
        # Maximum iterations per configuration
        self.max_iter = self.params_config.hyperband.max_iter
        # Defines configuration downsampling/elimination rate (default = 3)
        self.eta = self.params_config.hyperband.eta
        # number of times to run hyperband (brackets)
        self.s_max = int(math.log(self.max_iter) / math.log(self.eta)) + 1
        # i.e.  # of times to repeat the outer loops over the tradeoffs `s`
        self.B = self.s_max * self.max_iter  # budget per bracket of successive halving

        # if bounded:
        #     B = int(numpy.floor(logeta(max_units / min_units)) + 1) * max_units
        # else:
        #     B = int((2 ** k) * max_units)

    def get_number_of_configs(self, bracket):
        # n: initial number of configs
        return int(math.ceil((self.B / self.max_iter) * (self.eta ** bracket) / (bracket + 1)))

    def get_resources(self, bracket):
        # r: initial number of iterations/resources per config
        return self.max_iter * (self.eta ** (-bracket))

    def get_bracket(self, iteration):
        """This defines the bracket `s` in outerloop `for s in reversed(range(self.s_max))`."""
        return self.s_max - iteration

    def get_n_config_to_keep(self, n_suggestions, bracket_iteration):
        """Return the number of configs to keep and resume."""
        n_configs = n_suggestions * self.eta ** (-bracket_iteration)
        return int(n_configs / self.eta)

    def get_n_iteration(self, n_resources, bracket_iteration):
        """Returb the number of iterations to run for this barcket_i"""
        return n_resources * self.eta ** bracket_iteration

    def get_resources_for_iteration(self, iteration):
        bracket = self.get_bracket(iteration=iteration)
        return self.max_iter * (self.eta ** (-bracket))

    def get_n_config_to_keep_for_iteration(self, iteration, bracket_iteration):
        """Return the number of configs to keep for an iteration and iteration bracket.

        This is just util function around `get_n_config_to_keep`
        """
        bracket = self.get_bracket(iteration=iteration)
        bracket_iteration += 1
        if bracket_iteration == bracket:
            # End of loop `for bracket_iteration in range(bracket + 1):`
            return False

        n_configs = self.get_number_of_configs(bracket=bracket)
        return self.get_n_config_to_keep(
            n_suggestions=n_configs, bracket_iteration=bracket_iteration)

    def get_suggestions(self, iteration=None):
        """Return a list of suggestions/arms based on hyperband."""
        bracket = self.get_bracket(iteration=iteration)
        n_configs = self.get_number_of_configs(bracket=bracket)
        # n_resources = self.get_resources(bracket=bracket)
        return get_random_suggestions(matrix=self.params_config.matrix,
                                      n_suggestions=n_configs)

    def should_reschedule(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        if bracket_iteration >= 0:
            # The bracket is still processing
            return False

        # We can only reschedule if we can create a new bracket
        return self.get_bracket(iteration=iteration + 1) >= 0

    def should_reduce_configs(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another bracket iteration."""
        n_configs_to_keep = self.get_n_config_to_keep_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration)
        return n_configs_to_keep > 0
