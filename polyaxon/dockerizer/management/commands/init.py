import logging
import traceback

from django.core.management.base import BaseCommand

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from dockerizer.init import init
from dockerizer.utils import send_status

_logger = logging.getLogger('polyaxon.dockerizer.commands')


class Command(BaseCommand):
    """Management utility to start building a docker image."""
    help = 'Used to initialize a context to build a docker image.'

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

        # Initializing the docker context
        error = {}
        try:
            status = init(build_job=build_job)
            if not status:
                error = {
                    'raised': True,
                    'message': 'Failed to initialize build job job.'
                }
        except Exception as e:  # Other exceptions
            error = {
                'raised': True,
                'traceback': traceback.format_exc(),
                'message': 'Failed to build job encountered an {} exception'.format(
                    e.__class__.__name__)
            }

        if error.get('raised'):
            send_status(
                build_job=build_job,
                status=JobLifeCycle.FAILED,
                message=error.get('message'),
                traceback=error.get('traceback'))
            _logger.exception('Failed to create build job %s', error.get('traceback'))
            return
