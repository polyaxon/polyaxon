# # -*- coding: utf-8 -*-
# from __future__ import absolute_import, division, print_function
#
# import os
#
# from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
# from polyaxon_schemas.utils import TaskType
#
# from factories.factory_projects import ProjectFactory
# from spawner import K8SSpawner
# from spawner.templates.constants import DEFAULT_PORT
#
# from factories.factory_experiments import ExperimentFactory
#
# from tests.utils import BaseTest
#
#
# class TestSpawner(BaseTest):
#     def test_cluster(self):
#         plxfile = PolyaxonFile(os.path.abspath('tests/fixtures_static/advanced_file.yml'))
#         project = ProjectFactory()
#         experiment = ExperimentFactory(project=project,
#                                        config=plxfile.experiment_spec_at(0).parsed_data)
#         spawner = K8SSpawner(project_name=project.unique_name,
#                              experiment_name=experiment.unique_name,
#                              project_uuid=project.uuid.hex,
#                              experiment_uuid=experiment.uuid.hex,
#                              spec_config=experiment.config)
#
#         def job_name(task_type, task_idx):
#             return spawner.pod_manager.get_job_name(task_type, task_idx)
#
#         cluster_def = spawner.get_cluster().to_dict()
#         expected_cluster_def = {
#             TaskType.MASTER: ['{}:{}'.format(DEFAULT_PORT, job_name(TaskType.MASTER, 0))],
#             TaskType.WORKER: [
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.WORKER, 0)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.WORKER, 1)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.WORKER, 2)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.WORKER, 3)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.WORKER, 4)),
#             ],
#             TaskType.PS: [
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 0)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 1)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 2)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 3)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 4)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 5)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 6)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 7)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 8)),
#                 '{}:{}'.format(DEFAULT_PORT, job_name(TaskType.PS, 9)),
#             ]}
#         assert cluster_def == expected_cluster_def
