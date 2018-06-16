from django.contrib.admin import ModelAdmin


class ReadOnlyAdmin(ModelAdmin):
    """Disables all editing capabilities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pylint:disable=protected-access
        self.readonly_fields = [field.name for field in self.model._meta.get_fields()]

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass


class DiffModelAdmin(ModelAdmin):
    """Make diff model fields read-only."""
    readonly_fields = ('created_at', 'updated_at')
