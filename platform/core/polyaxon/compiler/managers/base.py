from rest_framework.exceptions import ValidationError

from schemas import PolyaxonSchemaError, ops_params


class BaseCompileManager(object):
    KIND = None
    SPECIFICATION = None

    @staticmethod
    def create_context_for_ref(param: ops_params.ParamSpec):
        from db.models.experiments import Experiment
        from db.models.jobs import Job

        if param.entity == ops_params.JOBS:
            Job.objects.filter(id=param.entity_ref)
        if param.entity == ops_params.EXPERIMENTS:
            Experiment.objects.filter(id=param.entity_ref)

    @staticmethod
    def create_context_for_spec(spec: 'BaseSpecification'):
        context = {}
        required_refs = spec.raw_config.get_params_with_refs()  # noqa
        return context

    @classmethod
    def validate_spec(cls, values: any):
        try:
            spec = cls.SPECIFICATION(values=values)  # pylint:disable=not-callable
            context = cls.create_context_for_spec(spec=spec)
            spec.apply_context(context=context)
            return spec
        except PolyaxonSchemaError as e:
            message_error = 'Received non valid specification config. %s' % e
            raise ValidationError(message_error)

    @classmethod
    def compile(cls, values: any) -> 'BaseSpecification':
        spec = cls.validate_spec(values=values)
        return spec
