from event_manager.event_service import EventService
from executor.handlers.build_job import BuildJobHandler
from executor.handlers.experiment import ExperimentHandler
from executor.handlers.experiment_group import ExperimentGroupHandler
from executor.handlers.job import JobHandler
from executor.handlers.notebook import NotebookHandler
from executor.handlers.tensorboard import TensorboardHandler
from executor.manager import default_manager


class ExecutorService(EventService):
    event_manager = default_manager

    HANDLER_MAPPING = {
        ExperimentHandler.SUBJECT: ExperimentHandler,
        ExperimentGroupHandler.SUBJECT: ExperimentGroupHandler,
        BuildJobHandler.SUBJECT: BuildJobHandler,
        JobHandler.SUBJECT: JobHandler,
        TensorboardHandler.SUBJECT: TensorboardHandler,
        NotebookHandler.SUBJECT: NotebookHandler,
    }

    def __init__(self):
        self.activity_log_manager = None

    def record_event(self, event):
        event_subject = event.get_event_subject()
        return self.HANDLER_MAPPING[event_subject].record_event(event=event)

    def setup(self):
        super().setup()
        # Load default event types
        import executor.events  # noqa
