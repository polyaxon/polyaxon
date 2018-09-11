import sys

from polyaxon_client.client import PolyaxonClient
from polyaxon_client.tracking.experiment import Experiment

client = PolyaxonClient(host='45.55.106.200',
                        token='db30d85a8b58c2fdec6ca0d4de1546942c689a44',
                        timeout=20)
experiment = Experiment(client=client, project='quick-start')
experiment.create(tags=['foo', 'bar'], description='ooooo')
experiment.log_params(activation='sigmoid', lr=0.11, range=10)
experiment.log_data_ref('foo', 'ofo')
experiment.log_data_ref('boo', 'boo')
# experiment.log_tags('foo, kay, goo, goo, goo', reset=True)
for i in range(10):
    experiment.log_metrics(**{'accuracy': 0.9872, 'precision': 0.9992237, 'loss': 0.03777724})
# raise ValueError('yeah')
