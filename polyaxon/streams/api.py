from sanic import Sanic

from streams.resources.builds import build_logs
from streams.resources.experiment_jobs import experiment_job_resources, experiment_job_logs
from streams.resources.experiments import experiment_resources, experiment_logs
from streams.resources.health import health
from streams.resources.jobs import job_logs

app = Sanic(__name__)


app.add_route(health, '/_health')

EXPERIMENT_URL = '/v1/<username>/<project_name>/experiments/<experiment_id>'
EXPERIMENT_JOB_URL = EXPERIMENT_URL + '/jobs/<job_id>'
BUILD_URL = '/v1/<username>/<project_name>/builds/<build_id>'
JOB_URL = '/v1/<username>/<project_name>/jobs/<job_id>'


def add_url(endpoint, base_url, url):
    app.add_websocket_route(endpoint, '{}/{}'.format(base_url, url))
    app.add_websocket_route(endpoint, '/ws{}/{}'.format(base_url, url))


# Experiment Job urls
add_url(endpoint=experiment_job_resources, base_url=EXPERIMENT_JOB_URL, url='resources')
add_url(endpoint=experiment_job_logs, base_url=EXPERIMENT_JOB_URL, url='logs')

# Experiment urls
add_url(endpoint=experiment_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=experiment_logs, base_url=EXPERIMENT_URL, url='logs')

# Job urls
# add_url(endpoint=job_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=job_logs, base_url=JOB_URL, url='logs')

# Build Job urls
# add_url(endpoint=job_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=build_logs, base_url=BUILD_URL, url='logs')


@app.listener('after_server_start')
async def notify_server_started(app, loop):  # pylint:disable=redefined-outer-name
    app.job_resources_ws_mangers = {}
    app.experiment_resources_ws_mangers = {}
    app.job_logs_consumers = {}
    app.experiment_logs_consumers = {}


@app.listener('after_server_stop')
async def notify_server_stopped(app, loop):  # pylint:disable=redefined-outer-name
    app.job_resources_ws_mangers = {}
    app.experiment_resources_ws_manger = {}

    consumer_keys = list(app.job_logs_consumers.keys())
    for consumer_key in consumer_keys:
        consumer = app.job_logs_consumers.pop(consumer_key, None)
        consumer.stop()

    consumer_keys = list(app.experiment_logs_consumers.keys())
    for consumer_key in consumer_keys:
        consumer = app.experiment_logs_consumers.pop(consumer_key, None)
        consumer.stop()
