import hyperopt

from marshmallow import ValidationError

from polyaxon.automl.matrix.utils import to_numpy
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
)


def to_hyperopt(name, matrix):
    if matrix.IDENTIFIER in {
        MatrixChoiceConfig.IDENTIFIER,
        MatrixRangeConfig.IDENTIFIER,
        MatrixLinSpaceConfig.IDENTIFIER,
        MatrixLogSpaceConfig.IDENTIFIER,
        MatrixGeomSpaceConfig.IDENTIFIER,
    }:
        return hyperopt.hp.choice(name, to_numpy(matrix))

    if matrix.IDENTIFIER == MatrixPChoiceConfig.IDENTIFIER:
        raise ValidationError(
            "{} is not supported by Hyperopt.".format(matrix.IDENTIFIER)
        )

    if matrix.IDENTIFIER == MatrixUniformConfig.IDENTIFIER:
        return hyperopt.hp.uniform(
            name, matrix.value.get("low"), matrix.value.get("high")
        )

    if matrix.IDENTIFIER == MatrixQUniformConfig.IDENTIFIER:
        return hyperopt.hp.quniform(
            name,
            matrix.value.get("low"),
            matrix.value.get("high"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == MatrixLogUniformConfig.IDENTIFIER:
        return hyperopt.hp.loguniform(
            name, matrix.value.get("low"), matrix.value.get("high")
        )

    if matrix.IDENTIFIER == MatrixQLogUniformConfig.IDENTIFIER:
        return hyperopt.hp.qloguniform(
            name,
            matrix.value.get("low"),
            matrix.value.get("high"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == MatrixNormalConfig.IDENTIFIER:
        return hyperopt.hp.normal(
            name, matrix.value.get("loc"), matrix.value.get("scale")
        )

    if matrix.IDENTIFIER == MatrixQNormalConfig.IDENTIFIER:
        return hyperopt.hp.qnormal(
            name,
            matrix.value.get("loc"),
            matrix.value.get("scale"),
            matrix.value.get("q"),
        )

    if matrix.IDENTIFIER == MatrixLogNormalConfig.IDENTIFIER:
        return hyperopt.hp.lognormal(
            name, matrix.value.get("loc"), matrix.value.get("scale")
        )

    if matrix.IDENTIFIER == MatrixQLogNormalConfig.IDENTIFIER:
        return hyperopt.hp.qlognormal(
            name,
            matrix.value.get("loc"),
            matrix.value.get("scale"),
            matrix.value.get("q"),
        )
