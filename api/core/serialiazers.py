# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import serializers

from core.models import (
    Experiment,
    RunConfig,
    InputData,
    Pipeline,
    Environment,
    Agent,
    Estimator,
    PolyaxonModel,
    Decoder,
    Encoder,
    SubGraph,
    Bridge,
    Optimizer,
    AgentMemory,
    Metric,
    Loss,
)


class LossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loss
        fields = ('id', 'module')


class LossDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loss
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('id', 'module')


class MetricDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'


class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = ('id', 'module')


class AgentMemoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = '__all__'


class OptimizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optimizer
        fields = ('id', 'module')


class OptimizerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Optimizer
        fields = '__all__'


class BridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridge
        fields = ('id', 'module')


class BridgeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridge
        fields = '__all__'


class SubGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGraph
        fields = ('id', 'module')


class SubGraphDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGraph
        fields = '__all__'


class EncoderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encoder
        fields = ('id', 'module')


class EncoderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encoder
        fields = '__all__'


class DecoderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoder
        fields = ('id', 'module')


class DecoderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoder
        fields = '__all__'


class PolyaxonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolyaxonModel
        fields = ('id', 'module')


class PolyaxonModelDetailSerializer(serializers.ModelSerializer):
    loss = LossDetailSerializer()
    eval_metrics = MetricDetailSerializer(many=True)
    optimizer = OptimizerDetailSerializer()
    graph = SubGraphDetailSerializer()
    encoder = EncoderDetailSerializer()
    decoder = DecoderDetailSerializer()
    bridge = BridgeDetailSerializer()

    class Meta:
        model = PolyaxonModel
        fields = '__all__'


class EstimatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimator
        fields = ('id', 'module')


class EstimatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimator
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('id', 'module')


class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'module')


class EnvironmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ('id', 'module')


class PipelineDataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'


class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = ('id',)


class InputDataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = '__all__'


class RunConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunConfig
        fields = ('id',)


class RunConfigDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunConfig
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('id', 'name',)


class ExperimentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class StatusSerializer(serializers.Serializer):
    job_id = serializers.CharField()
    status = serializers.CharField()
