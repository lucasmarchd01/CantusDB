from django.contrib import admin
from main_app.models import *
from main_app.forms import AdminChantForm

# these fields should not be editable by all classes
EXCLUDE = ("created_by", "last_updated_by", "json_info")


class BaseModelAdmin(admin.ModelAdmin):
    exclude = EXCLUDE

    # if an object is created in the admin interface, assign the user to the created_by field
    # else if an object is updated in the admin interface, assign the user to the last_updated_by field
    def save_model(self, request, obj, form, change):
        if change:
            obj.last_updated_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class CenturyAdmin(BaseModelAdmin):
    pass


class ChantAdmin(BaseModelAdmin):
    list_display = ("incipit", "get_source_siglum", "genre")
    search_fields = ("title", "incipit", "cantus_id")
    list_filter = ("genre",)
    exclude = EXCLUDE + (
        "col1",
        "col2",
        "col3",
        "next_chant",
        "s_sequence",
        "is_last_chant_in_feast",
        "visible_status"
    )
    form = AdminChantForm

    def get_source_siglum(self, obj):
        return obj.source.siglum


class FeastAdmin(BaseModelAdmin):
    search_fields = ("name", "feast_code")


class GenreAdmin(BaseModelAdmin):
    pass


class NotationAdmin(BaseModelAdmin):
    pass


class OfficeAdmin(BaseModelAdmin):
    pass


class ProvenanceAdmin(BaseModelAdmin):
    search_fields = ("name",)


class RismSiglumAdmin(BaseModelAdmin):
    pass


class SegmentAdmin(BaseModelAdmin):
    pass


class SequenceAdmin(BaseModelAdmin):
    search_fields = (
        "title",
        "incipit",
        "cantus_id",
    )
    exclude = EXCLUDE + ("c_sequence", "next_chant", "is_last_chant_in_feast")
    list_display = ("incipit", "get_source_siglum", "genre")
    list_filter = ("genre",)

    def get_source_siglum(self, obj):
        return obj.source.siglum


class SourceAdmin(BaseModelAdmin):
    # These search fields are also available on the user-source inline relationship in the user admin page
    search_fields = (
        "siglum",
        "title",
    )
    # from the Django docs:
    # Adding a ManyToManyField to this list will instead use a nifty unobtrusive JavaScript “filter” interface
    # that allows searching within the options. The unselected and selected options appear in two boxes side by side.
    filter_horizontal = (
        "century",
        "notation",
        "current_editors",
        "inventoried_by",
        "full_text_entered_by",
        "melodies_entered_by",
        "proofreaders",
        "other_editors",
    )


admin.site.register(Century, CenturyAdmin)
admin.site.register(Chant, ChantAdmin)
admin.site.register(Feast, FeastAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Notation, NotationAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Provenance, ProvenanceAdmin)
admin.site.register(RismSiglum, RismSiglumAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Source, SourceAdmin)
