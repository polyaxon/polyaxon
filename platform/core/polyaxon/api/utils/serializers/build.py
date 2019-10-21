class BuildMixin(object):

    def get_build_job(self, obj):
        return obj.build_job.unique_name if obj.build_job else None
