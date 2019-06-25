from schemas import ops_params


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
        required_refs = spec.raw_config.get_params_with_refs()
        return context

    @classmethod
    def compile(cls, content) -> 'BaseSpecification':
        spec = cls.SPECIFICATION(values=content)
        context = cls.create_context_for_spec(spec=spec)
        spec.parse_data(context=context)
        return spec
