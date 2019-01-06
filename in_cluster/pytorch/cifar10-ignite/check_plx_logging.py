# Polyaxon
from polyaxon_client.tracking import Experiment


experiment = Experiment()

print(experiment.get_experiment_info())

experiment.log_params(activation='sigmoid', lr=0.001)

experiment.log_params(dropout=0.5)

experiment.log_metrics(step=123, loss=0.023, accuracy=0.91)

experiment.log_data_ref(data="/data/cifar10-batches-py", data_name='my_dataset')
