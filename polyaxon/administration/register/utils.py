from django.contrib.admin import ModelAdmin


class ReadOnlyAdmin(ModelAdmin):
    """Disables all editing capabilities."""

    actions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pylint:disable=protected-access
        self.readonly_fields = [field.name for field in self.model._meta.get_fields()]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(ReadOnlyAdmin, self).change_view(request, object_id,
                                                      extra_context=extra_context)

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
