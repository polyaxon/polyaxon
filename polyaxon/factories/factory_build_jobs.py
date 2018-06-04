from faker import Factory as FakerFactory

import factory
from polyaxon_schemas.polyaxonfile.specification import BuildSpecification

from db.models.build_jobs import BuildJob
from factories.code_reference import CodeReferenceFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory

fake = FakerFactory.create()


class BuildJobFactory(factory.DjangoModelFactory):
    config = BuildSpecification.create_specification({'image': 'busybox'})

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    code_reference = factory.SubFactory(CodeReferenceFactory)

    class Meta:
        model = BuildJob
