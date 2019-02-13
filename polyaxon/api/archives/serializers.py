from api.build_jobs.serializers import BookmarkedBuildJobSerializer
from api.experiment_groups.serializers import BookmarkedExperimentGroupSerializer
from api.experiments.serializers import BookmarkedExperimentSerializer
from api.jobs.serializers import BookmarkedJobSerializer
from api.projects.serializers import BookmarkedProjectSerializer


class ArchivedBuildJobSerializer(BookmarkedBuildJobSerializer):
    class Meta(BookmarkedBuildJobSerializer.Meta):
        fields = BookmarkedBuildJobSerializer.Meta.fields + ('deleted',)


class ArchivedJobSerializer(BookmarkedJobSerializer):
    class Meta(BookmarkedJobSerializer.Meta):
        fields = BookmarkedJobSerializer.Meta.fields + ('deleted',)


class ArchivedExperimentSerializer(BookmarkedExperimentSerializer):
    class Meta(BookmarkedExperimentSerializer.Meta):
        fields = BookmarkedExperimentSerializer.Meta.fields + ('deleted',)


class ArchivedExperimentGroupSerializer(BookmarkedExperimentGroupSerializer):
    class Meta(BookmarkedExperimentGroupSerializer.Meta):
        fields = BookmarkedExperimentGroupSerializer.Meta.fields + ('deleted',)


class ArchivedProjectSerializer(BookmarkedProjectSerializer):
    class Meta(BookmarkedProjectSerializer.Meta):
        fields = BookmarkedProjectSerializer.Meta.fields + ('deleted',)
