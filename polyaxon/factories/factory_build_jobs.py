from faker import Factory as FakerFactory

import factory

from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from factories.factorycode_reference import CodeReferenceFactory
from polyaxon_schemas.polyaxonfile.specification import BuildSpecification

fake = FakerFactory.create()


class BuildJobFactory(factory.DjangoModelFactory):
    config = BuildSpecification.create_specification({'image': 'busybox'})

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    code_reference = factory.SubFactory(CodeReferenceFactory)

    class Meta:
        model = BuildJob


class BuildJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(BuildJobFactory)

    class Meta:
        model = BuildJobStatus
