from rest_framework import serializers


class UserMixin(serializers.Serializer):

    def get_user(self, obj):
        return obj.user.username
