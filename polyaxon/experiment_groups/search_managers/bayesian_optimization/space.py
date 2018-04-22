""" module for algorithm manager """

import numpy as np

from polyaxon_schemas.utils import Optimization


def deal_with_categorical(feasible_values, one_hot_values):
    """ function to do the one hot encoding of the categorical values """
    index = np.argmax(one_hot_values)
    return feasible_values[index]


class SearchSpace(object):
    def __init__(self, params_config, iteration_config):
        self.params_config = params_config
        self.iteration_config = iteration_config
        self._dim = 0
        self._lowerbound = []
        self._upperbound = []
        self._names = []
        # record all the feasible values of discrete type variables
        self._discrete_info = {}
        self._categorical_info = {}

        self.set_bounds()

    def set_bounds(self):
        for key, value in self.params_config.matrix.items():
            self._names.append(key)
            # one hot encoding for categorical type
            if value.is_categorical:
                values = value.to_numpy()
                num_feasible = len(values)
                for _ in range(num_feasible):
                    self._lowerbound.append(0)
                    self._upperbound.append(1)
                self._categorical_info[key] = {
                    "values": values,
                    "number": num_feasible,
                }
                self._dim += num_feasible
            elif value.is_discrete:
                self._dim = self._dim + 1
                discrete_values = value.to_numpy()
                self._lowerbound.append(value.min)
                self._upperbound.append(value.max)
                self._discrete_info[key] = {
                    "values": discrete_values,
                }
            elif value.is_unifrom:
                self._dim = self._dim + 1
                self._lowerbound.append(float(value.min))
                self._upperbound.append(float(value.max))

    def parse_y(self, y):
        if not y:
            return y
        y_values = []
        for value in y:
            if Optimization.maximize(self.params_config.bo.metric.optimization):
                y_values.append(float(value))
            else:
                y_values.append(-float(value))

        return y_values

    @staticmethod
    def parse_x(x):
        if not x:
            return x

        return np.array(x)

    def _get_discrete_suggestion(self, name, suggestion, counter):
        feasible_values = self._discrete_info[name]["values"]
        current_value = suggestion[counter]

        diff = np.subtract(feasible_values, current_value)
        diff = np.absolute(diff)
        results = feasible_values[np.argmin(diff)]
        return results, counter + 1

    def _get_categorical_suggestion(self, name, suggestion, counter):
        one_hot_values = suggestion[counter:counter + self._categorical_info[name]["number"]]
        index = np.argmax(one_hot_values)
        feasible_values = self._discrete_info[name]["values"]
        results = feasible_values[index]
        return results, counter + self._categorical_info[name]["number"]

    def get_next_suggestion(self, suggestion):
        counter = 0
        results = []
        for name in self._names:
            if name in self._discrete_info:
                result, counter = self._get_discrete_suggestion(
                    name=name,
                    suggestion=suggestion[counter],
                    counter=counter)
                results.append(result)

            elif name in self._categorical_info:
                result, counter = self._get_categorical_suggestion(
                    name=name,
                    suggestion=suggestion[counter],
                    counter=counter)
                results.append(result)
            else:
                results.append(suggestion[counter])
                counter = counter + 1
        return results

    def to_dict(self, x_next):
        return dict(zip(self._names, x_next))
