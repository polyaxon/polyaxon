from faker import Factory as FakerFactory

import factory

from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from schemas import BuildSpecification

fake = FakerFactory.create()


class BuildJobFactory(factory.DjangoModelFactory):
    content = BuildSpecification.create_specification({'image': 'busybox'}, to_dict=False).raw_data

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    code_reference = factory.SubFactory(CodeReferenceFactory)

    class Meta:
        model = BuildJob


class BuildJobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(BuildJobFactory)

    class Meta:
        model = BuildJobStatus
