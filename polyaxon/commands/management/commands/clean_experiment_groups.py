from constants.experiment_groups import ExperimentGroupLifeCycle
from db.models.experiment_groups import ExperimentGroup
from libs.base_clean import BaseCleanCommand
from scheduler.tasks.experiment_groups import experiments_group_stop_experiments


class Command(BaseCleanCommand):
    @staticmethod
    def _clean():
        for experiment_group in ExperimentGroup.objects.filter(
                status__status__in=ExperimentGroupLifeCycle.RUNNING_STATUS):
            experiments_group_stop_experiments(
                experiment_group_id=experiment_group.project_id,
                pending=True,
                message='Cleanup')
