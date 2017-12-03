# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from kubernetes import watch

from events.tasks import handle_events_namespace

logger = logging.getLogger('polyaxon.monitors.namespace')

LEVEL_MAPPING = {
    'normal': 'info',
}


def run(k8s_manager, cluster):
    w = watch.Watch()

    for event in w.stream(k8s_manager.k8s_api.list_namespaced_event,
                          namespace=k8s_manager.namespace):
        logger.debug("event: %s" % event)

        event_type = event['type'].lower()
        event = event['object']

        meta = {
            k: v for k, v
            in event.metadata.to_dict().items()
            if v is not None
        }

        creation_timestamp = meta.pop('creation_timestamp', None)

        level = (event.type and event.type.lower())
        level = LEVEL_MAPPING.get(level, level)

        component = source_host = reason = short_name = kind = None
        if event.source:
            source = event.source.to_dict()

            if 'component' in source:
                component = source['component']
            if 'host' in source:
                source_host = source['host']

        if event.reason:
            reason = event.reason

        if event.involved_object and event.involved_object.name:
            name = event.involved_object.name
            bits = name.split('-')
            if len(bits) in (1, 2):
                short_name = bits[0]
            else:
                short_name = "-".join(bits[:-2])

        if event.involved_object and event.involved_object.kind:
            kind = event.involved_object.kind

        message = event.message

        if short_name:
            obj_name = "({}/{})".format(k8s_manager.namespace, short_name)
        else:
            obj_name = "({})".format(k8s_manager.namespace)

        if level in ('warning', 'error') or event_type in ('error',):
            if event.involved_object:
                meta['involved_object'] = {
                    k: v for k, v
                    in event.involved_object.to_dict().items()
                    if v is not None
                }

            data = {
                'server_name': source_host or 'n/a',
                'obj_name': obj_name,
                'message': message
            }

            if component:
                data['component'] = component

            if short_name:
                data['name'] = short_name

            if kind:
                data['kind'] = kind

            if reason:
                data['reason '] = reason

            payload = dict(
                create_at=creation_timestamp,
                data=data,
                meta=meta,
                level=level,
            )

            logger.info("Publishing event: {}".format(data))
            handle_events_namespace.delay(cluster_id=cluster.id, payload=payload)
