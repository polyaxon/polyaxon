from options import option_namespaces, option_subjects
from options.feature import Feature
from options.option import NAMESPACE_DB_OPTION_MARKER

FEATURES_POLYFLOW_STORE = '{}{}{}{}{}'.format(option_namespaces.FEATURES,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_namespaces.POLYFLOW,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.HUB)


class FeaturesPolyflowStore(Feature):
    key = FEATURES_POLYFLOW_STORE


FEATURES_POLYFLOW_PIPELINES = '{}{}{}{}{}'.format(option_namespaces.FEATURES,
                                                  NAMESPACE_DB_OPTION_MARKER,
                                                  option_namespaces.POLYFLOW,
                                                  NAMESPACE_DB_OPTION_MARKER,
                                                  option_subjects.PIPELINES)


class FeaturesPolyflowPipelines(Feature):
    key = FEATURES_POLYFLOW_PIPELINES
