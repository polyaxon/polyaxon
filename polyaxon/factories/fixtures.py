from polyaxon_schemas.polyaxonfile.specification import (
    ExperimentSpecification,
    JobSpecification,
    NotebookSpecification,
    TensorboardSpecification,
    BuildSpecification)

# flake8: noqa

experiment_group_spec_content = """---
    version: 1
    
    kind: group

    hptuning:
      matrix:
        lr:
          logspace: 0.01:0.1:5

    model:
      model_type: regressor
      loss:
        MeanSquaredError:
      optimizer:
        Adam:
          learning_rate: "{{ lr }}"
      graph:
        input_layers: images
        layers:
          - Conv2D:
              filters: 64
              kernel_size: [3, 3]
              strides: [1, 1]
              activation: relu
              kernel_initializer: Ones
          - MaxPooling2D:
              kernels: 2
          - Flatten:
          - Dense:
              units: 10
              activation: softmax

    train:
      data_pipeline:
        TFRecordImagePipeline:
          batch_size: 64
          num_epochs: 1
          shuffle: true
          dynamic_pad: false
          data_files: ["../data/mnist/mnist_train.tfrecord"]
          meta_data_file: "../data/mnist/meta_data.json"
"""

experiment_group_spec_content_2_xps = """---
    version: 1
    
    kind: group
      
    hptuning:
      concurrency: 2
      matrix:
        lr:
          values: [0.01, 0.1]

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""

experiment_group_spec_content_early_stopping = """---
    version: 1
    
    kind: group

    hptuning:
      concurrency: 2
      random_search:
        n_experiments: 2
      early_stopping:
        - metric: precision
          value: 0.9
        - metric: loss
          value: 0.1
          optimization: minimize 
      matrix:
        lr:
          values: [0.01, 0.1, 0.5]

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""

experiment_group_spec_content_hyperband = """---
    version: 1

    kind: group

    hptuning:
      concurrency: 2
      hyperband:
        max_iter: 5
        eta: 3
        resource:
          name: steps
          type: int
        metric: 
          name: loss
          optimization: minimize
        resume: False
      early_stopping:
        - metric: precision
          value: 0.9
        - metric: loss
          value: 0.1
          optimization: minimize 
      matrix:
        lr:
          values: [0.01, 0.1, 0.5]

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""


experiment_group_spec_content_hyperband_trigger_reschedule = """---
    version: 1

    kind: group

    hptuning:
      concurrency: 200
      hyperband:
        max_iter: 10
        eta: 3
        resource:
          name: steps
          type: int
        metric: 
          name: loss
          optimization: minimize
        resume: False
      early_stopping:
        - metric: precision
          value: 0.9
        - metric: loss
          value: 0.1
          optimization: minimize 
      matrix:
        lr:
          values: [0.01, 0.1, 0.5]
        feature2: 
          linspace: [1, 2, 5]
        feature3: 
          range: [1, 5, 1]
        feature4: 
          range: [1, 5, 1]

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""


experiment_group_spec_content_bo = """---
    version: 1

    kind: group

    hptuning:
      concurrency: 2
      bo:
        n_iterations: 5
        n_initial_trials: 2
        metric: 
          name: loss
          optimization: minimize
        utility_function:
          acquisition_function: ucb
          kappa: 1.2
          gaussian_process:
            kernel: matern
            length_scale: 1.0
            nu: 1.9
            n_restarts_optimizer: 0
      early_stopping:
        - metric: precision
          value: 0.9
        - metric: loss
          value: 0.1
          optimization: minimize 
      matrix:
        lr:
          values: [0.01, 0.1, 0.5]

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""


experiment_spec_content = """---
    version: 1
    
    kind: experiment

    model:
      model_type: regressor
      loss:
        MeanSquaredError:
      optimizer:
        Adam:
          learning_rate: 0.7
      graph:
        input_layers: images
        layers:
          - Conv2D:
              filters: 64
              kernel_size: [3, 3]
              strides: [1, 1]
              activation: relu
              kernel_initializer: Ones
          - MaxPooling2D:
              kernels: 2
          - Flatten:
          - Dense:
              units: 10
              activation: softmax

    train:
      data_pipeline:
        TFRecordImagePipeline:
          batch_size: 64
          num_epochs: 1
          shuffle: true
          dynamic_pad: false
          data_files: ["../data/mnist/mnist_train.tfrecord"]
          meta_data_file: "../data/mnist/meta_data.json"
"""
experiment_spec_parsed_content = ExperimentSpecification.read(experiment_spec_content)

exec_experiment_spec_content = """---
    version: 1
    
    kind: experiment

    build:
      image: my_image
    
    run:
      cmd: video_prediction_train --model=DNA --num_masks=1
"""

exec_experiment_spec_parsed_content = ExperimentSpecification.read(exec_experiment_spec_content)


exec_experiment_resources_content = """---
    version: 1
    
    kind: experiment

    declarations:
      lr: 0.1
      dropout: 0.5
    
    environment:
      resources:
        cpu:
          requests: 1
          limits: 1    
        memory:
          requests: 100
          limits: 200
    
      tensorflow:  
        n_workers: 1
        n_ps: 1  
        
        default_worker_resources:
          cpu:
            requests: 1
            limits: 1
            
          memory:
            requests: 100
            limits: 200
        
        default_ps_resources:
          cpu:
            requests: 1
            limits: 1
            
          memory:
            requests: 100
            limits: 200

    model:
      model_type: regressor
      loss:
        MeanSquaredError:
      optimizer:
        Adam:
          learning_rate: 0.7
      graph:
        input_layers: images
        layers:
          - Conv2D:
              filters: 64
              kernel_size: [3, 3]
              strides: [1, 1]
              activation: relu
              kernel_initializer: Ones
          - MaxPooling2D:
              kernels: 2
          - Flatten:
          - Dense:
              units: 10
              activation: softmax

    train:
      data_pipeline:
        TFRecordImagePipeline:
          batch_size: 64
          num_epochs: 1
          shuffle: true
          dynamic_pad: false
          data_files: ["../data/mnist/mnist_train.tfrecord"]
          meta_data_file: "../data/mnist/meta_data.json"
"""
exec_experiment_resources_parsed_content = ExperimentSpecification.read(
    exec_experiment_resources_content)


tensorboard_spec_content = """---
    version: 1
    
    kind: tensorboard

    build:
      image: my_image
"""

tensorboard_spec_parsed_content = TensorboardSpecification.read(tensorboard_spec_content)


notebook_spec_content = """---
    version: 1

    kind: notebook

    build:
      image: my_image
"""

notebook_spec_parsed_content = NotebookSpecification.read(notebook_spec_content)


job_spec_content = """---
    version: 1

    kind: job

    build:
      image: my_image
    
    run:
      cmd: test
"""

job_spec_parsed_content = JobSpecification.read(job_spec_content)


job_spec_resources_content = """---
    version: 1

    kind: job
    
    environment:
      resources:
        cpu:
          requests: 1
          limits: 1    
        memory:
          requests: 100
          limits: 200

    build:
      image: my_image

    run:
      cmd: test
"""

job_spec_resources_parsed_content = JobSpecification.read(job_spec_resources_content)

build_spec_content = """---
    version: 1

    kind: build

    build:
      image: my_image
      build_steps: ['step1', 'step2']
"""

build_spec_parsed_content = BuildSpecification.read(build_spec_content)
