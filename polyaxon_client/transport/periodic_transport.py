# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.logger import logger
from polyaxon_client.transport.retry_transport import RetryTransportMixin
from polyaxon_client.workers.periodic_worker import PeriodicWorker


class PeriodicTransportMixin(RetryTransportMixin):
    """Threads operations transport."""

    @property
    def done(self):
        if hasattr(self, '_periodic_done'):
            return self._periodic_done
        return None

    @property
    def exceptions(self):
        if hasattr(self, '_periodic_exceptions'):
            return self._periodic_exceptions
        return None

    def queue_request(self, request, url, **kwargs):
        try:
            request(url=url, session=self.retry_session, **kwargs)
        except Exception as e:
            self._periodic_exceptions += 1
            logger.debug('Error making request url: %s, params: params %s, exp: %s', url, kwargs, e)
        finally:
            self._periodic_done += 1

    @property
    def periodic_workers(self):
        if not hasattr(self, '_periodic_workers'):
            self._periodic_workers = {}

        return self._periodic_workers

    def get_periodic_worker(self, url, **kwargs):
        worker = self.periodic_workers.get(url)
        if not worker or not worker.is_alive():
            if 'request' not in kwargs:
                raise PolyaxonClientException('Periodic worker expects a request argument.')
            kwargs['url'] = url
            worker = PeriodicWorker(callback=self.queue_request,
                                    worker_interval=self.config.interval,
                                    worker_timeout=self.config.timeout,
                                    kwargs=kwargs)
            worker.start()
            self.periodic_workers[url] = worker
        return self.periodic_workers[url]

    def periodic_post(self,
                      url,
                      params=None,
                      data=None,
                      files=None,
                      json_data=None,
                      timeout=None,
                      headers=None):
        """Periodic Async Call request with a post."""
        worker = self.get_periodic_worker(url=url,
                                          request=self.post,
                                          params=params,
                                          files=files,
                                          timeout=timeout,
                                          headers=headers)
        return worker.queue(data=data, json_data=json_data)
