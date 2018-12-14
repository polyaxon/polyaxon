# from sidecar import settings
#
#
# def start_experiment_sidecar(monitor, k8s_manager, pod_id, labels):
#     monitor.run_for_experiment_job(
#         k8s_manager=k8s_manager,
#         pod_id=pod_id,
#         experiment_uuid=labels.experiment_uuid.hex,
#         experiment_name=labels.experiment_name,
#         job_uuid=labels.job_uuid.hex,
#         task_type=labels.task_type,
#         task_idx=labels.task_idx,
#         container_job_name=settings.CONTAINER_NAME_EXPERIMENT_JOB)
#
#
# def start_job_side_car(monitor, k8s_manager, pod_id, labels):
#     monitor.run_for_job(k8s_manager=k8s_manager,
#                         pod_id=pod_id,
#                         job_name=labels.job_name,
#                         job_uuid=labels.job_uuid.hex,
#                         container_job_name=settings.CONTAINER_NAME_JOB)
