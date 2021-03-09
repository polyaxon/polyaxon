#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Union

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.client.decorators import client_handler
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.tracking.run import Run

TRACKING_RUN = None


def init(
    owner: str = None,
    project: str = None,
    run_uuid: str = None,
    client: RunClient = None,
    track_code: bool = True,
    track_env: bool = True,
    refresh_data: bool = False,
    artifacts_path: str = None,
    collect_artifacts: str = None,
    collect_resources: str = None,
    is_offline: bool = None,
    is_new: bool = None,
    name: str = None,
    description: str = None,
    tags: List[str] = None,
):
    """Tracking module is similar to the tracking client without the need to create a run instance.

    The tracking module allows you to call all tracking methods directly from the top level module.

    This could be very convenient especially if you are running in-cluster experiments:

    ```python
    from polyaxon import tracking

    tracking.init()
    ...
    tracking.log_metrics(step=1, loss=0.09, accuracy=0.75)
    ...
    tracking.log_metrics(step=1, loss=0.02, accuracy=0.85)
    ...
    ```

    > A global `TRACKING_RUN` will be set on the module.


        Args:
            owner: str, optional, the owner is the username or
                the organization name owning this project.
            project: str, optional, project name owning the run(s).
            run_uuid: str, optional, run uuid.
            client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/), optional,
                an instance of a configured client, if not passed,
                a new instance will be created based on the available environment.
            track_code: bool, optional, default True, to track code version.
                Polyaxon will try to track information about any repo
                configured in the context where this client is instantiated.
            track_env: bool, optional, default True, to track information about the environment.
            refresh_data: bool, optional, default False, to refresh the run data at instantiation.
            refresh_data: bool, optional, default False, to instruct the run to resume,
                only useful when the run is not managed by Polyaxon.
            artifacts_path: str, optional, for in-cluster runs it will be set automatically.
            collect_artifacts: bool, optional,
                similar to the env var flag `POLYAXON_COLLECT_ARTIFACTS`, this env var is `True`
                by default for managed runs and is controlled by the plugins section.
            collect_resources: bool, optional,
                similar to the env var flag `POLYAXON_COLLECT_RESOURCES`, this env var is `True`
                by default for managed runs and is controlled by the plugins section.
            is_offline: bool, optional,
                To trigger the offline mode manually instead of depending on `POLYAXON_IS_OFFLINE`.
            is_new: bool, optional,
                Force the creation of a new run instead of trying to discover a cached run or
                refreshing an instance from the env var
            name: str, optional,
                When `is_new` or `is_offline` is set to true, a new instance is created and
                you can initialize that new run with a name.
            description: str, optional,
                When `is_new` or `is_offline` is set to true, a new instance is created and
                you can initialize that new run with a description.
            tags: str or List[str], optional,
                When `is_new` or `is_offline` is set to true, a new instance is created and
                you can initialize that new run with tags.

        Raises:
            PolyaxonClientException: If no owner and/or project are passed and Polyaxon cannot
                resolve the values from the environment.
    """
    global TRACKING_RUN

    TRACKING_RUN = Run(
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        client=client,
        track_code=track_code,
        refresh_data=refresh_data,
        track_env=track_env,
        artifacts_path=artifacts_path,
        collect_artifacts=collect_artifacts,
        collect_resources=collect_resources,
        is_offline=is_offline,
        is_new=is_new,
        name=name,
        description=description,
        tags=tags,
    )


@client_handler(check_no_op=True)
def get_or_create_run(tracking_run: Run = None) -> Optional[Run]:
    """Get or create a new tracking run.

    It tries to create a new instance, for in-cluster runs, this will work automatically.

    This is used inside some Polyaxon callbacks, you should use `init` instead.
    """
    global TRACKING_RUN

    if tracking_run:
        return tracking_run
    if TRACKING_RUN:
        return TRACKING_RUN

    if settings.CLIENT_CONFIG.is_managed:
        init()
        return TRACKING_RUN


def get_artifacts_path(
    rel_path: str = None, ensure_path: bool = False, is_dir: bool = False
):
    global TRACKING_RUN
    return TRACKING_RUN.get_artifacts_path(
        rel_path=rel_path,
        ensure_path=ensure_path,
        is_dir=is_dir,
    )


get_artifacts_path.__doc__ = Run.get_artifacts_path.__doc__


def get_outputs_path(
    rel_path: str = None, ensure_path: bool = True, is_dir: bool = False
):
    global TRACKING_RUN
    return TRACKING_RUN.get_outputs_path(
        rel_path=rel_path,
        ensure_path=ensure_path,
        is_dir=is_dir,
    )


get_outputs_path.__doc__ = Run.get_outputs_path.__doc__


def get_tensorboard_path(rel_path: str = "tensorboard"):
    global TRACKING_RUN
    return TRACKING_RUN.get_tensorboard_path(rel_path=rel_path)


get_tensorboard_path.__doc__ = Run.get_tensorboard_path.__doc__


def set_artifacts_path(artifacts_path: str, is_related: bool = False):
    global TRACKING_RUN
    TRACKING_RUN.set_artifacts_path(artifacts_path, is_related)


set_artifacts_path.__doc__ = Run.set_artifacts_path.__doc__


def set_run_event_logger():
    global TRACKING_RUN
    TRACKING_RUN.set_run_event_logger()


set_run_event_logger.__doc__ = Run.set_run_event_logger.__doc__


def set_run_resource_logger():
    global TRACKING_RUN
    TRACKING_RUN.set_run_resource_logger()


set_run_resource_logger.__doc__ = Run.set_run_resource_logger.__doc__


def log_metric(name: str, value: float, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_metric(
        name=name,
        value=value,
        step=step,
        timestamp=timestamp,
    )


log_metric.__doc__ = Run.log_metric.__doc__


def log_metrics(step: int = None, timestamp: datetime = None, **metrics):
    global TRACKING_RUN
    TRACKING_RUN.log_metrics(step=step, timestamp=timestamp, **metrics)


log_metrics.__doc__ = Run.log_metrics.__doc__


def log_roc_auc_curve(
    name: str, fpr, tpr, auc: float = None, step: int = None, timestamp: datetime = None
):
    global TRACKING_RUN
    TRACKING_RUN.log_roc_auc_curve(
        name=name,
        fpr=fpr,
        tpr=tpr,
        auc=auc,
        step=step,
        timestamp=timestamp,
    )


log_roc_auc_curve.__doc__ = Run.log_roc_auc_curve.__doc__


def log_sklearn_roc_auc_curve(
    name: str,
    y_preds,
    y_targets,
    step: int = None,
    timestamp: datetime = None,
    is_multi_class: bool = False,
):
    global TRACKING_RUN
    TRACKING_RUN.log_sklearn_roc_auc_curve(
        name=name,
        y_preds=y_preds,
        y_targets=y_targets,
        step=step,
        timestamp=timestamp,
        is_multi_class=is_multi_class,
    )


log_sklearn_roc_auc_curve.__doc__ = Run.log_sklearn_roc_auc_curve.__doc__


def log_pr_curve(
    name: str,
    precision,
    recall,
    average_precision=None,
    step: int = None,
    timestamp: datetime = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_pr_curve(
        name=name,
        precision=precision,
        recall=recall,
        average_precision=average_precision,
        step=step,
        timestamp=timestamp,
    )


log_pr_curve.__doc__ = Run.log_pr_curve.__doc__


def log_sklearn_pr_curve(
    name: str,
    y_preds,
    y_targets,
    step: int = None,
    timestamp: datetime = None,
    is_multi_class: bool = False,
):
    global TRACKING_RUN
    TRACKING_RUN.log_sklearn_pr_curve(
        name=name,
        y_preds=y_preds,
        y_targets=y_targets,
        step=step,
        timestamp=timestamp,
        is_multi_class=is_multi_class,
    )


log_sklearn_pr_curve.__doc__ = Run.log_sklearn_pr_curve.__doc__


def log_curve(
    name: str,
    x,
    y,
    annotation: str = None,
    step: int = None,
    timestamp: datetime = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_curve(
        name=name,
        x=x,
        y=y,
        annotation=annotation,
        step=step,
        timestamp=timestamp,
    )


log_curve.__doc__ = Run.log_curve.__doc__


def log_image(
    data: Any,
    name: str = None,
    step: int = None,
    timestamp: datetime = None,
    rescale=1,
    dataformats: str = "CHW",
):
    global TRACKING_RUN
    TRACKING_RUN.log_image(
        data=data,
        name=name,
        step=step,
        timestamp=timestamp,
        rescale=rescale,
        dataformats=dataformats,
    )


log_image.__doc__ = Run.log_image.__doc__


def log_image_with_boxes(
    tensor_image,
    tensor_boxes,
    name: str = None,
    step: int = None,
    timestamp: datetime = None,
    rescale: int = 1,
    dataformats: str = "CHW",
):
    global TRACKING_RUN
    TRACKING_RUN.log_image_with_boxes(
        tensor_image=tensor_image,
        tensor_boxes=tensor_boxes,
        name=name,
        step=step,
        timestamp=timestamp,
        rescale=rescale,
        dataformats=dataformats,
    )


log_image_with_boxes.__doc__ = Run.log_image_with_boxes.__doc__


def log_mpl_image(
    data,
    name: str = None,
    close: bool = True,
    step: int = None,
    timestamp: datetime = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_mpl_image(
        data=data,
        name=name,
        close=close,
        step=step,
        timestamp=timestamp,
    )


log_mpl_image.__doc__ = Run.log_mpl_image.__doc__


def log_video(
    data,
    name: str = None,
    fps: int = 4,
    step: int = None,
    timestamp: datetime = None,
    content_type: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_video(
        data=data,
        name=name,
        fps=fps,
        step=step,
        timestamp=timestamp,
        content_type=content_type,
    )


log_video.__doc__ = Run.log_video.__doc__


def log_audio(
    data,
    name: str = None,
    sample_rate: int = 44100,
    step: int = None,
    timestamp: datetime = None,
    content_type: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_audio(
        data=data,
        name=name,
        sample_rate=sample_rate,
        step=step,
        timestamp=timestamp,
        content_type=content_type,
    )


log_audio.__doc__ = Run.log_audio.__doc__


def log_text(name: str, text: str, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_text(
        name=name,
        text=text,
        step=step,
        timestamp=timestamp,
    )


log_text.__doc__ = Run.log_text.__doc__


def log_html(name: str, html: str, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_html(
        name=name,
        html=html,
        step=step,
        timestamp=timestamp,
    )


log_html.__doc__ = Run.log_html.__doc__


def log_np_histogram(
    name: str, values, counts, step: int = None, timestamp: datetime = None
):
    global TRACKING_RUN
    TRACKING_RUN.log_np_histogram(
        name=name,
        values=values,
        counts=counts,
        step=step,
        timestamp=timestamp,
    )


log_np_histogram.__doc__ = Run.log_np_histogram.__doc__


def log_histogram(
    name: str, values, bins, max_bins=None, step: int = None, timestamp: datetime = None
):
    global TRACKING_RUN
    TRACKING_RUN.log_histogram(
        name=name,
        values=values,
        bins=bins,
        max_bins=max_bins,
        step=step,
        timestamp=timestamp,
    )


log_histogram.__doc__ = Run.log_histogram.__doc__


def log_model(
    path: str,
    name: str = None,
    framework: str = None,
    summary: Dict = None,
    step: int = None,
    timestamp: datetime = None,
    rel_path: str = "model",
    versioned: bool = True,
):
    global TRACKING_RUN
    TRACKING_RUN.log_model(
        path=path,
        name=name,
        framework=framework,
        summary=summary,
        step=step,
        timestamp=timestamp,
        rel_path=rel_path,
        versioned=versioned,
    )


log_model.__doc__ = Run.log_model.__doc__


def log_artifact(
    path: str,
    name: str = None,
    kind: str = None,
    summary: Dict = None,
    step: int = None,
    timestamp: datetime = None,
    rel_path: str = None,
    versioned: bool = True,
    **kwargs
):
    global TRACKING_RUN
    TRACKING_RUN.log_artifact(
        path=path,
        name=name,
        kind=kind,
        summary=summary,
        step=step,
        timestamp=timestamp,
        rel_path=rel_path,
        versioned=versioned,
        **kwargs,
    )


log_artifact.__doc__ = Run.log_artifact.__doc__


def log_dataframe(
    path: str,
    name: str = None,
    content_type: str = None,
    step: int = None,
    timestamp: datetime = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_dataframe(
        path=path,
        name=name,
        content_type=content_type,
        step=step,
        timestamp=timestamp,
    )


log_dataframe.__doc__ = Run.log_dataframe.__doc__


def log_plotly_chart(name: str, figure, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_plotly_chart(
        name=name,
        figure=figure,
        step=step,
        timestamp=timestamp,
    )


log_plotly_chart.__doc__ = Run.log_plotly_chart.__doc__


def log_bokeh_chart(name: str, figure, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_bokeh_chart(
        name=name,
        figure=figure,
        step=step,
        timestamp=timestamp,
    )


log_bokeh_chart.__doc__ = Run.log_bokeh_chart.__doc__


def log_altair_chart(name: str, figure, step: int = None, timestamp: datetime = None):
    global TRACKING_RUN
    TRACKING_RUN.log_altair_chart(
        name=name,
        figure=figure,
        step=step,
        timestamp=timestamp,
    )


log_altair_chart.__doc__ = Run.log_altair_chart.__doc__


def log_mpl_plotly_chart(
    name: str, figure, step: int = None, timestamp: datetime = None
):
    global TRACKING_RUN
    TRACKING_RUN.log_mpl_plotly_chart(
        name=name,
        figure=figure,
        step=step,
        timestamp=timestamp,
    )


log_mpl_plotly_chart.__doc__ = Run.log_mpl_plotly_chart.__doc__


def get_log_level():
    global TRACKING_RUN
    return TRACKING_RUN.get_log_level()


get_log_level.__doc__ = Run.get_log_level.__doc__


def set_description(description: str, async_req: bool = True):
    global TRACKING_RUN
    TRACKING_RUN.set_description(description=description, async_req=async_req)


set_description.__doc__ = Run.set_description.__doc__


def set_name(name: str, async_req: bool = True):
    global TRACKING_RUN
    TRACKING_RUN.set_name(name=name, async_req=async_req)


set_name.__doc__ = Run.set_name.__doc__


def end():
    global TRACKING_RUN
    TRACKING_RUN.end()


end.__doc__ = Run.end.__doc__


def log_status(
    status: str,
    reason: str = None,
    message: str = None,
    last_transition_time: datetime = None,
    last_update_time: datetime = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_status(
        status=status,
        reason=reason,
        message=message,
        last_transition_time=last_transition_time,
        last_update_time=last_update_time,
    )


log_status.__doc__ = Run.log_status.__doc__


def log_inputs(reset: bool = False, async_req: bool = True, **inputs):
    global TRACKING_RUN
    TRACKING_RUN.log_inputs(reset=reset, async_req=async_req, **inputs)


log_inputs.__doc__ = Run.log_inputs.__doc__


def log_outputs(reset: bool = False, async_req: bool = True, **outputs):
    global TRACKING_RUN
    TRACKING_RUN.log_outputs(reset=reset, async_req=async_req, **outputs)


log_outputs.__doc__ = Run.log_outputs.__doc__


def log_tags(
    tags: Union[str, Sequence[str]],
    reset: bool = False,
    async_req: bool = True,
):
    global TRACKING_RUN
    TRACKING_RUN.log_tags(tags=tags, reset=reset, async_req=async_req)


log_tags.__doc__ = Run.log_tags.__doc__


def log_meta(reset: bool = False, async_req: bool = True, **meta):
    global TRACKING_RUN
    TRACKING_RUN.log_meta(reset=reset, async_req=async_req, **meta)


log_meta.__doc__ = Run.log_meta.__doc__


def log_succeeded():
    global TRACKING_RUN
    TRACKING_RUN.log_succeeded()


log_succeeded.__doc__ = Run.log_succeeded.__doc__


def log_stopped():
    global TRACKING_RUN
    TRACKING_RUN.log_stopped()


log_stopped.__doc__ = Run.log_stopped.__doc__


def log_failed(reason: str = None, message: str = None):
    global TRACKING_RUN
    TRACKING_RUN.log_failed(reason=reason, message=message)


log_failed.__doc__ = Run.log_failed.__doc__


def log_artifact_ref(
    path: str,
    kind: V1ArtifactKind,
    name: str = None,
    hash: str = None,
    content=None,
    summary: Dict = None,
    is_input: bool = False,
    rel_path: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_artifact_ref(
        path=path,
        kind=kind,
        name=name,
        hash=hash,
        content=content,
        summary=summary,
        is_input=is_input,
        rel_path=rel_path,
    )


log_artifact_ref.__doc__ = Run.log_artifact_ref.__doc__


def log_model_ref(
    path: str,
    name: str = None,
    framework: str = None,
    summary: Dict = None,
    is_input: bool = False,
    rel_path: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_model_ref(
        path=path,
        name=name,
        framework=framework,
        summary=summary,
        is_input=is_input,
        rel_path=rel_path,
    )


log_model_ref.__doc__ = Run.log_model_ref.__doc__


def log_code_ref(code_ref: Dict = None, is_input: bool = True):
    global TRACKING_RUN
    TRACKING_RUN.log_code_ref(code_ref=code_ref, is_input=is_input)


log_code_ref.__doc__ = Run.log_code_ref.__doc__


def log_data_ref(
    name: str,
    hash: str = None,
    path: str = None,
    content=None,
    summary: Dict = None,
    is_input: bool = True,
):
    global TRACKING_RUN
    TRACKING_RUN.log_data_ref(
        name=name,
        content=content,
        hash=hash,
        path=path,
        summary=summary,
        is_input=is_input,
    )


log_data_ref.__doc__ = Run.log_data_ref.__doc__


def log_file_ref(
    path: str,
    name: str = None,
    hash: str = None,
    content=None,
    summary: Dict = None,
    is_input: bool = True,
    rel_path: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_file_ref(
        path=path,
        name=name,
        hash=hash,
        content=content,
        summary=summary,
        is_input=is_input,
        rel_path=rel_path,
    )


log_file_ref.__doc__ = Run.log_file_ref.__doc__


def log_dir_ref(
    path: str,
    name: str = None,
    summary: Dict = None,
    is_input: bool = False,
    rel_path: str = None,
):
    global TRACKING_RUN
    TRACKING_RUN.log_dir_ref(
        path=path, name=name, summary=summary, is_input=is_input, rel_path=rel_path
    )


log_dir_ref.__doc__ = Run.log_dir_ref.__doc__


def log_artifact_lineage(body: List[V1RunArtifact]):
    global TRACKING_RUN
    TRACKING_RUN.log_artifact_lineage(body)


log_artifact_lineage.__doc__ = Run.log_artifact_lineage.__doc__


def log_env(rel_path: str = None, content: Dict = None):
    global TRACKING_RUN
    return TRACKING_RUN.log_env(rel_path=rel_path, content=content)


log_env.__doc__ = Run.log_env.__doc__


def sync_events_summaries():
    global TRACKING_RUN
    TRACKING_RUN.sync_events_summaries()


sync_events_summaries.__doc__ = Run.sync_events_summaries.__doc__


def sync_offline_run(
    artifacts_path: str = None,
    load_offline_run: bool = False,
):
    global TRACKING_RUN
    TRACKING_RUN.sync_offline_run(
        artifacts_path=artifacts_path,
        load_offline_run=load_offline_run,
    )


sync_offline_run.__doc__ = Run.sync_offline_run.__doc__
