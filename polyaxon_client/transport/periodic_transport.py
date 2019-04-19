# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.logger import logger
from polyaxon_client.transport.retry_transport import RetryTransportMixin
from polyaxon_client.workers.periodic_worker import PeriodicWorker


class PeriodicHttpTransportMixin(RetryTransportMixin):
    """Periodic http operations transport."""

    @property
    def periodic_http_done(self):
        if hasattr(self, '_periodic_http_done'):
            return self._periodic_http_done
        return None

    @property
    def periodic_http_exceptions(self):
        if hasattr(self, '_periodic_http_exceptions'):
            return self._periodic_http_exceptions
        return None

    def queue_periodic_request(self, request, url, **kwargs):
        try:
            request(url=url, session=self.retry_session, **kwargs)
        except Exception as e:
            self._periodic_http_exceptions += 1
            logger.debug('Error making request url: %s, params: params %s, exp: %s', url, kwargs, e)
        finally:
            self._periodic_http_done += 1

    @property
    def periodic_http_worker(self):
        if hasattr(self, '_periodic_http_worker'):
            return self._periodic_http_worker
        return None

    def get_periodic_http_worker(self, **kwargs):
        worker = self.periodic_http_worker
        if not worker or not worker.is_alive():
            if 'request' not in kwargs:
                raise PolyaxonClientException('Periodic worker expects a request argument.')
            self._periodic_http_worker = PeriodicWorker(
                callback=self.queue_periodic_request,
                worker_interval=self.config.interval,
                worker_timeout=self.config.timeout,
                kwargs=kwargs)
            self._periodic_http_worker.start()
        return self.periodic_http_worker

    def set_health_check(self, url):
        worker = self.get_periodic_http_worker(request=self.post)
        worker.queue_health(url)

    def unset_health_check(self, url):
        worker = self.get_periodic_http_worker(request=self.post)
        worker.unqueue_health(url)

    def periodic_post(self,
                      url,
                      params=None,
                      data=None,
                      files=None,
                      json_data=None,
                      timeout=None,
                      headers=None):
        """Periodic Async Call request with a post."""
        worker = self.get_periodic_http_worker(request=self.post,
                                               params=params,
                                               files=files,
                                               timeout=timeout,
                                               headers=headers)
        return worker.queue(url=url, data=data, json_data=json_data)


class PeriodicWSTransportMixin(RetryTransportMixin):
    """Periodic websocket operations transport."""

    @property
    def periodic_ws_done(self):
        if hasattr(self, '_periodic_ws_done'):
            return self._periodic_ws_done
        return None

    @property
    def periodic_ws_exceptions(self):
        if hasattr(self, '_periodic_ws_exceptions'):
            return self._periodic_ws_exceptions
        return None

    def queue_ws_request(self, request, url, **kwargs):
        try:
            request(url=url, **kwargs)
        except Exception as e:
            self._periodic_ws_exceptions += 1
            logger.debug('Error making request url: %s, params: params %s, exp: %s', url, kwargs, e)
        finally:
            self._periodic_ws_done += 1

    @property
    def periodic_ws_workers(self):
        if not hasattr(self, '_periodic_ws_workers'):
            self._periodic_ws_workers = {}

        return self._periodic_ws_workers

    def get_periodic_http_worker(self, url, **kwargs):
        worker = self.periodic_ws_workers.get(url)
        if not worker or not worker.is_alive():
            kwargs['url'] = url
            kwargs['request'] = self.socket(url, message_handler=None, **kwargs)
            worker = PeriodicWorker(callback=self.queue_ws_request,
                                    worker_interval=self.config.interval,
                                    worker_timeout=self.config.timeout,
                                    kwargs=kwargs)
            worker.start()
            self.periodic_ws_workers[url] = worker
        return self.periodic_ws_workers[url]

    def periodic_send(self, url, data=None, headers=None):
        """Periodic Async Call request with a post."""
        worker = self.get_periodic_http_worker(url=url, headers=headers)
        return worker.queue(data=data)
