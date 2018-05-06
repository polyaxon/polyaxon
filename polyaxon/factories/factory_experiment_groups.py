import factory

from experiment_groups.models import ExperimentGroup, ExperimentGroupStatus
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from factories.fixtures import experiment_group_spec_content_2_xps


class ExperimentGroupFactory(factory.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    content = experiment_group_spec_content_2_xps

    class Meta:
        model = ExperimentGroup


class ExperimentGroupStatusFactory(factory.DjangoModelFactory):
    experiment_group = factory.SubFactory(ExperimentGroup)

    class Meta:
        model = ExperimentGroupStatus
