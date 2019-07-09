from db.models.experiment_groups import ExperimentGroup

groups = ExperimentGroup.objects.select_related(
    'status',
)
groups = groups.prefetch_related(
    'user',
    'project',
    'project__user',
)
groups_details = groups
