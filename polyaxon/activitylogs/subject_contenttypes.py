from collections import namedtuple

from event_manager import event_subjects


class EventContenttype(namedtuple("EventContenttype", "app_label model")):

    def items(self):
        return self._asdict().items()


mapping = {
    event_subjects.CLUSTER: EventContenttype(app_label='clusters',
                                             model='cluster'),
    event_subjects.CLUSTER_NODE: EventContenttype(app_label='nodes',
                                                  model='clusternode'),
    event_subjects.EXPERIMENT: EventContenttype(app_label='experiments',
                                                model='experiment'),
    event_subjects.EXPERIMENT_GROUP: EventContenttype(app_label='experiment_groups',
                                                      model='experimentgroup'),
    event_subjects.EXPERIMENT_JOB: EventContenttype(app_label='experiments',
                                                    model='experimentjob'),
    event_subjects.NOTEBOOK: EventContenttype(app_label='plugins',
                                              model='notebookjob'),
    event_subjects.PROJECT: EventContenttype(app_label='projects',
                                             model='project'),
    event_subjects.REPO: EventContenttype(app_label='repos',
                                          model='repo'),
    event_subjects.SUPERUSER: EventContenttype(app_label='auth',
                                               model='user'),
    event_subjects.TENSORBOARD: EventContenttype(app_label='plugins',
                                                 model='tensorboardjob'),
    event_subjects.USER: EventContenttype(app_label='auth',
                                          model='user'),
}
