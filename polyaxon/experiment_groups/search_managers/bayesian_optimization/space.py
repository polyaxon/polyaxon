""" module for algorithm manager """

import numpy as np

from polyaxon_schemas.utils import Optimization


class SearchSpace(object):
    def __init__(self, params_config):
        self.params_config = params_config
        self._dim = 0
        self._bounds = []
        self._names = []
        self._discrete_info = {}
        self._categorical_info = {}
        self._x = []
        self._y = []

        self.set_bounds()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def bounds(self):
        return self._bounds

    def set_bounds(self):
        bounds = []
        for key, value in self.params_config.matrix.items():
            self._names.append(key)
            # one hot encoding for categorical type
            if value.is_categorical:
                values = value.to_numpy()
                num_feasible = len(values)
                for _ in range(num_feasible):
                    bounds.append((0, 1))
                self._categorical_info[key] = {
                    "values": values,
                    "number": num_feasible,
                }
                self._dim += num_feasible
            elif value.is_discrete:
                self._dim = self._dim + 1
                discrete_values = value.to_numpy()
                bounds.append((value.min, value.max))
                self._discrete_info[key] = {
                    "values": discrete_values,
                }
            elif value.is_unifrom:
                self._dim = self._dim + 1
                bounds.append((float(value.min), float(value.max)))
        self._bounds = np.asarray(bounds)

    def parse_y(self, metrics):
        if not metrics:
            return metrics
        y_values = []
        for value in metrics:
            if Optimization.maximize(self.params_config.bo.metric.optimization):
                y_values.append(float(value))
            else:
                y_values.append(-float(value))

        return y_values

    def parse_x(self, configs):
        if not configs:
            return configs
        x = []
        for config in configs:
            for name in self._names:
                if name in self._discrete_info:
                    x += [1 if v == config[name] else 0
                          for v in self._discrete_info[name]['values']]
                elif name in self._names:
                    x.append(config[name])
        return np.array(x)

    def add_observations(self, configs, metrics):
        self._x = self.parse_x(configs=configs)
        self._y = self.parse_y(metrics=metrics)

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

    def get_suggestion(self, suggestion):
        counter = 0
        results = []
        for name in self._names:
            if name in self._discrete_info:
                result, counter = self._get_discrete_suggestion(
                    name=name,
                    suggestion=suggestion,
                    counter=counter)
                results.append(result)

            elif name in self._categorical_info:
                result, counter = self._get_categorical_suggestion(
                    name=name,
                    suggestion=suggestion,
                    counter=counter)
                results.append(result)
            else:
                results.append(suggestion[counter])
                counter = counter + 1
        return dict(zip(self._names, results))
