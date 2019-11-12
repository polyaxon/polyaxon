import copy
import numpy as np

from marshmallow import ValidationError

from polyaxon.automl.matrix import dist
from polyaxon.schemas.polyflow.workflows.matrix import (
    MatrixChoiceConfig,
    MatrixGeomSpaceConfig,
    MatrixLinSpaceConfig,
    MatrixLogNormalConfig,
    MatrixLogSpaceConfig,
    MatrixLogUniformConfig,
    MatrixNormalConfig,
    MatrixPChoiceConfig,
    MatrixQLogNormalConfig,
    MatrixQLogUniformConfig,
    MatrixQNormalConfig,
    MatrixQUniformConfig,
    MatrixRangeConfig,
    MatrixUniformConfig,
    pchoice,
)


def space_sample(value, size, rand_generator):
    size = None if size == 1 else size
    rand_generator = rand_generator or np.random
    try:
        return rand_generator.choice(value, size=size)
    except ValueError:
        idx = rand_generator.randint(0, len(value))
        return value[idx]


def dist_sample(fct, value, size, rand_generator):
    size = None if size == 1 else size
    rand_generator = rand_generator or np.random
    value = copy.deepcopy(value)
    value["size"] = size
    value["rand_generator"] = rand_generator
    return fct(**value)


def get_length(matrix):
    if matrix.IDENTIFIER == MatrixChoiceConfig.IDENTIFIER:
        return len(matrix.value)
    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        return len(matrix.value)

    if matrix.IDENTIFIER == MatrixRangeConfig.IDENTIFIER:
        return len(np.arange(**matrix.value))

    if matrix.IDENTIFIER == MatrixLinSpaceConfig.IDENTIFIER:
        return len(np.linspace(**matrix.value))

    if matrix.IDENTIFIER == MatrixLogSpaceConfig.IDENTIFIER:
        return len(np.logspace(**matrix.value))

    if matrix.IDENTIFIER == MatrixGeomSpaceConfig.IDENTIFIER:
        return len(np.geomspace(**matrix.value))

    if matrix.IDENTIFIER in {
        MatrixUniformConfig.IDENTIFIER,
        MatrixQUniformConfig.IDENTIFIER,
        MatrixLogUniformConfig.IDENTIFIER,
        MatrixQLogUniformConfig.IDENTIFIER,
        MatrixNormalConfig.IDENTIFIER,
        MatrixQNormalConfig.IDENTIFIER,
        MatrixLogNormalConfig.IDENTIFIER,
        MatrixQLogNormalConfig.IDENTIFIER,
    }:
        raise ValidationError("Distribution should not call `length`")


def get_min(matrix):
    if matrix.IDENTIFIER == MatrixChoiceConfig.IDENTIFIER:
        if matrix.is_categorical:
            return None
        return min(to_numpy(matrix))

    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        return None

    if matrix.IDENTIFIER in {
        MatrixRangeConfig.IDENTIFIER,
        MatrixLinSpaceConfig.IDENTIFIER,
        MatrixLogSpaceConfig.IDENTIFIER,
        MatrixGeomSpaceConfig.IDENTIFIER,
    }:
        return matrix.value.get("start")

    if matrix.IDENTIFIER == MatrixUniformConfig.IDENTIFIER:
        return matrix.value.get("low")

    if matrix.IDENTIFIER in {
        MatrixQUniformConfig.IDENTIFIER,
        MatrixLogUniformConfig.IDENTIFIER,
        MatrixQLogUniformConfig.IDENTIFIER,
        MatrixNormalConfig.IDENTIFIER,
        MatrixQNormalConfig.IDENTIFIER,
        MatrixLogNormalConfig.IDENTIFIER,
        MatrixQLogNormalConfig.IDENTIFIER,
    }:
        return None


def get_max(matrix):
    if matrix.IDENTIFIER == MatrixChoiceConfig.IDENTIFIER:
        if matrix.is_categorical:
            return None
        return max(to_numpy(matrix))

    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        return None

    if matrix.IDENTIFIER in {
        MatrixRangeConfig.IDENTIFIER,
        MatrixLinSpaceConfig.IDENTIFIER,
        MatrixLogSpaceConfig.IDENTIFIER,
        MatrixGeomSpaceConfig.IDENTIFIER,
    }:
        return matrix.value.get("stop")

    if matrix.IDENTIFIER == MatrixUniformConfig.IDENTIFIER:
        return matrix.value.get("high")

    if matrix.IDENTIFIER in {
        MatrixQUniformConfig.IDENTIFIER,
        MatrixLogUniformConfig.IDENTIFIER,
        MatrixQLogUniformConfig.IDENTIFIER,
        MatrixNormalConfig.IDENTIFIER,
        MatrixQNormalConfig.IDENTIFIER,
        MatrixLogNormalConfig.IDENTIFIER,
        MatrixQLogNormalConfig.IDENTIFIER,
    }:
        return None


def to_numpy(matrix):
    if matrix.IDENTIFIER == MatrixChoiceConfig.IDENTIFIER:
        return matrix.value
    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        raise ValidationError(
            "Distribution should not call `to_numpy`, "
            "instead it should call `sample`."
        )

    if matrix.IDENTIFIER == MatrixRangeConfig.IDENTIFIER:
        return np.arange(**matrix.value)

    if matrix.IDENTIFIER == MatrixLinSpaceConfig.IDENTIFIER:
        return np.linspace(**matrix.value)

    if matrix.IDENTIFIER == MatrixLogSpaceConfig.IDENTIFIER:
        return np.logspace(**matrix.value)

    if matrix.IDENTIFIER == MatrixGeomSpaceConfig.IDENTIFIER:
        return np.geomspace(**matrix.value)

    if matrix.IDENTIFIER in {
        MatrixUniformConfig.IDENTIFIER,
        MatrixQUniformConfig.IDENTIFIER,
        MatrixLogUniformConfig.IDENTIFIER,
        MatrixQLogUniformConfig.IDENTIFIER,
        MatrixNormalConfig.IDENTIFIER,
        MatrixQNormalConfig.IDENTIFIER,
        MatrixLogNormalConfig.IDENTIFIER,
        MatrixQLogNormalConfig.IDENTIFIER,
    }:
        raise ValidationError(
            "Distribution should not call `to_numpy`, "
            "instead it should call `sample`."
        )


def sample(matrix, size=None, rand_generator=None):
    size = None if size == 1 else size

    if matrix.IDENTIFIER == MatrixChoiceConfig.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )
    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        return pchoice(values=matrix.value, size=size, rand_generator=rand_generator)

    if matrix.IDENTIFIER == MatrixRangeConfig.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == MatrixLinSpaceConfig.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == MatrixLogSpaceConfig.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == MatrixGeomSpaceConfig.IDENTIFIER:
        return space_sample(
            value=to_numpy(matrix), size=size, rand_generator=rand_generator
        )

    if matrix.IDENTIFIER == MatrixUniformConfig.IDENTIFIER:
        return dist_sample(dist.uniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixQUniformConfig.IDENTIFIER:
        return dist_sample(dist.quniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixLogUniformConfig.IDENTIFIER:
        return dist_sample(dist.loguniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixQLogUniformConfig.IDENTIFIER:
        return dist_sample(dist.qloguniform, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixNormalConfig.IDENTIFIER:
        return dist_sample(dist.normal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixQNormalConfig.IDENTIFIER:
        return dist_sample(dist.qnormal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixLogNormalConfig.IDENTIFIER:
        return dist_sample(dist.lognormal, matrix.value, size, rand_generator)

    if matrix.IDENTIFIER == MatrixQLogNormalConfig.IDENTIFIER:
        return dist_sample(dist.qlognormal, matrix.value, size, rand_generator)
