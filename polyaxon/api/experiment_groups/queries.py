from db.models.experiment_groups import ExperimentGroup

groups = ExperimentGroup.objects.select_related(
    'user',
    'project',
    'project__user',
    'status',
)
groups_details = groups
