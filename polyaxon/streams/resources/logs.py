import asyncio
import json

from kubernetes_asyncio import client, config

from constants.jobs import JobLifeCycle
from logs_handlers.log_queries.base import process_log_line
from streams.constants import SOCKET_SLEEP
from streams.resources.utils import notify, get_status_message, notify_ws, should_disconnect
from streams.socket_manager import SocketManager


async def log_job(request, ws, job, pod_id, namespace, container):
    job_uuid = job.uuid.hex
    if job_uuid in request.app.job_logs_ws_managers:
        ws_manager = request.app.job_logs_ws_managers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_logs_ws_managers[job_uuid] = ws_manager

    ws_manager.add_socket(ws)

    # Stream phase changes
    status = None
    while status != JobLifeCycle.RUNNING and not JobLifeCycle.is_done(status):
        job.refresh_from_db()
        if status != job.last_status:
            status = job.last_status
            await notify_ws(ws=ws, message=get_status_message(status))
            if should_disconnect(ws=ws, ws_manager=ws_manager):
                return
        await asyncio.sleep(SOCKET_SLEEP)

    if JobLifeCycle.is_done(status):
        await notify_ws(ws=ws, message=get_status_message(status))
        return

    config.load_incluster_config()
    k8s_api = client.CoreV1Api()
    await log_job_pod(k8s_api=k8s_api,
                      ws=ws,
                      ws_manager=ws_manager,
                      pod_id=pod_id,
                      container=container,
                      namespace=namespace)


async def log_job_pod(k8s_api, ws, ws_manager, pod_id, container, namespace):
    resp = await k8s_api.read_namespaced_pod_log(pod_id,
                                                 namespace,
                                                 container=container,
                                                 follow=True,
                                                 _preload_content=False,
                                                 timestamps=True)
    should_quite = False
    while True:
        try:
            log_line = await resp.content.readline()
        except asyncio.TimeoutError:
            log_line = None
        if not log_line:
            break
        log_line = process_log_line(log_line=log_line.decode('utf-8'))
        await notify(ws_manager, json.dumps({'log_lines': log_line}))

        if should_disconnect(ws=ws, ws_manager=ws_manager):
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(0.001)
