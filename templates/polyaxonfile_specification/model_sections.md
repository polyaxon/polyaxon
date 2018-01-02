The model section defines a different way to run experiments
on Polyaxon without the need of code.

When using the model section in you polyaxon files, you don't need to define a [run section](sections#run).

A model is defined as the following:

 * model_type [required]: the type of the model, could be a [Classifier](/polyaxon_lib/models#classifier), [Regressor](/polyaxon_lib/models#regressor), or [Generator](/polyaxon_lib/models#generator).
 * loss [optional]: the loss function to use, [possible values](polyaxon_lib/losses)
 * metrics [optional]: the list of metrics to use, [possible values](polyaxon_lib/metrics)
 * optimizer [optional]: the optimizer to use, [possible values](polyaxon_lib/optimizers)
 * graph [required]: the graph definition.
    * inputs [required]: list of tensors that graph expects as inputs.
    * outpus [optonal]: list of tensors the graph outputs.
    * layers [required]: a list of layers, [possible values](polyaxon_lib/layers)


Example:

```yaml
model:
  model_type: classifier
  loss: MeanSquaredError
  optimizer:
    Adam:
      learning_rate: 0.21
  graph:
    input_layers: images
    layers:
      - for:
          len: "{{ cnn.kernels|length }}"
          do:
            - Conv2D:
                filters: "{{ cnn.kernels[index] }}"
                kernel_size: "{{ cnn.size }}"
                strides: "{{ cnn.strides }}"
                activation: relu
                tags: tag1

      - if:
          cond: 1 == 1
          do:
            MaxPooling2D:
              kernels: 12

      - if:
          cond: "32 == {{ cnn.kernels[1] }}"
          do:
            for:
              len: "{{ cnn.kernels|length }}"
              do:
                - Conv2D:
                    filters: "{{ cnn.kernels[index] }}"
                    kernel_size: "{{ cnn.size }}"
                    strides: "{{ cnn.strides }}"
                    activation: relu
                    tags: tag2
                    is_output: true
          else_do:
            MaxPooling2D:
              kernels: 12
              is_output: true

      - Flatten:
          inbound_nodes: ["{{ tags.tag1[1] }}"]
      - Dense:
          units: 10
          activation: softmax
          name: super_dense
```
