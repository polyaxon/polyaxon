from collections import OrderedDict

from rest_framework.exceptions import ValidationError

from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.outputs import OutputsRefs


def get_valid_ref(model, instance=None, entity_id=None, entity_args=None):
    if entity_id:
        return model.objects.filter(id=entity_id).values_list('id', flat=True)
    elif entity_args:
        if len(entity_args) == 1:
            return model.objects.filter(
                project=instance.project, name=entity_args[0]).values_list('id', flat=True)
        elif len(entity_args) == 2:
            return model.objects.filter(
                project__user=instance.user,
                project__name=entity_args[0],
                name=entity_args[1]).values_list('id', flat=True)
        elif len(entity_args) == 3:
            return model.objects.filter(
                project__user__username=entity_args[0],
                project__name=entity_args[1],
                name=entity_args[2]).values_list('id', flat=True)
    return None


def raise_invalid_ref(enitity, enitity_ref):
    raise ValidationError('Could not find a valid reference to entity `{}`: {}'.format(
        enitity,
        enitity_ref
    ))


def get_valid_outputs(instance, outputs, model, entity):
    validated_outputs = []
    for output_value in outputs:
        try:
            output = int(output_value)
            output_ref = get_valid_ref(model=model, entity_id=output)
        except (TypeError, ValueError):
            if '.' in output_value:
                output = output_value.split('.')
                output_ref = get_valid_ref(instance=instance, model=model, entity_args=output)
            elif '/' in output_value:
                output = output_value.split('/')
                output_ref = get_valid_ref(instance=instance, model=model, entity_args=output)
            else:
                output_ref = get_valid_ref(instance=instance,
                                           model=model,
                                           entity_args=[output_value])
        if not output_ref:
            raise_invalid_ref(entity, output_value)
        validated_outputs.append(output_ref[0])

    return validated_outputs


def set_outputs(instance):
    if instance.outputs:
        outputs_config = instance.outputs_config
    elif instance.specification and instance.specification.outputs:
        outputs_config = instance.specification.outputs
    else:
        return

    # Validate the outputs
    if outputs_config.jobs:
        jobs = get_valid_outputs(instance=instance,
                                 outputs=outputs_config.jobs,
                                 model=Job,
                                 entity='Job')
        outputs_config.jobs = list(OrderedDict.fromkeys(jobs))

    if outputs_config.experiments:
        experiments = get_valid_outputs(instance=instance,
                                        outputs=outputs_config.experiments,
                                        model=Experiment,
                                        entity='Experiment')
        outputs_config.experiments = list(OrderedDict.fromkeys(experiments))
    instance.outputs = outputs_config.to_dict()


def set_outputs_refs(instance):
    if not instance.outputs:
        return

    if not instance.outputs_jobs and not instance.outputs_experiments:
        return

    outputs_refs = OutputsRefs.objects.create()
    if instance.outputs_jobs:
        outputs_refs.jobs.add(*instance.outputs_jobs)
    if instance.outputs_experiments:
        outputs_refs.experiments.add(*instance.outputs_experiments)

    instance.outputs_refs = outputs_refs
