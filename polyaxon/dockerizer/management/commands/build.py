import logging

from docker.errors import DockerException

from django.core.management.base import BaseCommand

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from dockerizer import builder

_logger = logging.getLogger('polyaxon.dockerizer.commands')


class Command(BaseCommand):
    """Management utility to start building a docker image."""
    help = 'Used to build a docker image.'

    def add_arguments(self, parser):
        parser.add_argument('build_job_uuid')
        super().add_arguments(parser)

    def handle(self, *args, **options):
        build_job_uuid = options['build_job_uuid']
        try:
            build_job = BuildJob.objects.get(uuid=build_job_uuid)
        except BuildJob.DoesNotExist:
            self.stdout.write(
                'The build job %s does not exist anymore.' % build_job_uuid,
                ending='\n')
            return

        # Building the docker image
        try:
            status = builder.build(build_job=build_job)
        except DockerException as e:
            builder.send_status(
                build_job=build_job,
                status=JobLifeCycle.FAILED,
                message='Failed to build job %s' % e)
            _logger.exception('Failed to build job %s', e)
            status = False
        except Exception as e:  # Other exceptions
            builder.send_status(
                build_job=build_job,
                status=JobLifeCycle.FAILED,
                message='Failed to build job %s' % e)
            _logger.exception('Failed to create build job %s', e)
            status = False

        if not status:
            builder.send_status(
                build_job=build_job,
                status=JobLifeCycle.FAILED,
                message='Failed to build job.')
            return

        builder.send_status(
            build_job=build_job,
            status=JobLifeCycle.SUCCEEDED)
