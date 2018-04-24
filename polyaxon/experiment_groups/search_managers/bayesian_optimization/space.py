import numpy as np

from polyaxon_schemas.utils import Optimization


class SearchSpace(object):
    def __init__(self, params_config):
        self.params_config = params_config
        self._dim = 0
        self._bounds = []
        self._features = []
        self._discrete_features = {}
        self._categorical_features = {}
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
    def dim(self):
        return self._dim

    @property
    def features(self):
        return self._features

    @property
    def discrete_features(self):
        return self._discrete_features

    @property
    def categorical_features(self):
        return self._categorical_features

    @property
    def bounds(self):
        return self._bounds

    def set_bounds(self):
        bounds = []
        for key in sorted(self.params_config.matrix.keys()):
            value = self.params_config.matrix[key]
            self._features.append(key)
            # one hot encoding for categorical type
            if value.is_categorical:
                values = value.to_numpy()
                num_feasible = len(values)
                for _ in range(num_feasible):
                    bounds.append((0, 1))
                self._categorical_features[key] = {
                    "values": values,
                    "number": num_feasible,
                }
                self._dim += num_feasible
            elif value.is_discrete:
                self._dim = self._dim + 1
                discrete_values = value.to_numpy()
                bounds.append((value.min, value.max))
                self._discrete_features[key] = {
                    "values": discrete_values,
                }
            elif value.is_uniform:
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

        return np.array(y_values)

    def parse_x(self, configs):
        if not configs:
            return configs
        x = []
        for config in configs:
            x_config = []
            for feature in self._features:
                if feature in self._categorical_features:
                    x_config += [1 if v == config[feature] else 0
                                 for v in self._categorical_features[feature]['values']]
                elif feature in self._features:
                    x_config.append(config[feature])
            x.append(x_config)
        return np.array(x)

    def add_observations(self, configs, metrics):
        self._x = self.parse_x(configs=configs)
        self._y = self.parse_y(metrics=metrics)

    def _get_discrete_suggestion(self, feature, suggestion, counter):
        feasible_values = self._discrete_features[feature]["values"]
        current_value = suggestion[counter]

        diff = np.subtract(feasible_values, current_value)
        diff = np.absolute(diff)
        results = feasible_values[np.argmin(diff)]
        return results, counter + 1

    def _get_categorical_suggestion(self, feature, suggestion, counter):
        one_hot_values = suggestion[counter:counter + self._categorical_features[feature]["number"]]
        index = np.argmax(one_hot_values)
        feasible_values = self._categorical_features[feature]["values"]
        results = feasible_values[index]
        return results, counter + self._categorical_features[feature]["number"]

    def get_suggestion(self, suggestion):
        counter = 0
        results = []
        for feature in self._features:
            if feature in self._discrete_features:
                result, counter = self._get_discrete_suggestion(
                    feature=feature,
                    suggestion=suggestion,
                    counter=counter)
                results.append(result)

            elif feature in self._categorical_features:
                result, counter = self._get_categorical_suggestion(
                    feature=feature,
                    suggestion=suggestion,
                    counter=counter)
                results.append(result)
            else:
                results.append(suggestion[counter])
                counter = counter + 1
        return dict(zip(self._features, results))
