from faker import Factory as FakerFactory

import factory

from db.models.jobs import Job, JobStatus
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from factories.fixtures import job_spec_parsed_content

fake = FakerFactory.create()


class JobFactory(factory.DjangoModelFactory):
    config = job_spec_parsed_content.parsed_data

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Job


class JobStatusFactory(factory.DjangoModelFactory):
    job = factory.SubFactory(JobFactory)

    class Meta:
        model = JobStatus
