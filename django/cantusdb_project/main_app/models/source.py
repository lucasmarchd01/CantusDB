from django.db import models
from main_app.models import BaseModel, Segment
from django.contrib.auth import get_user_model


class Source(BaseModel):
    cursus_choices = [("Monastic", "Monastic"), ("Secular", "Secular")]
    source_status_choices = [
        (
            "Editing process (not all the fields have been proofread)",
            "Editing process (not all the fields have been proofread)",
        ),
        ("Published / Complete", "Published / Complete"),
        ("Published / Proofread pending", "Published / Proofread pending"),
        ("Unpublished / Editing process", "Unpublished / Editing process"),
        ("Unpublished / Indexing process", "Unpublished / Indexing process"),
        ("Unpublished / Proofread pending", "Unpublished / Proofread pending"),
        ("Unpublished / Proofreading process", "Unpublished / Proofreading process"),
        ("Unpublished / No indexing activity", "Unpublished / No indexing activity"),
    ]

    # The old Cantus uses two fields to jointly control the access to sources.
    # Here in the new Cantus, we only use one field, and there are two levels: published and unpublished.
    # Published sources are available to the public.
    # Unpublished sources are hidden from the list and cannot be accessed by URL until the user logs in.
    published = models.BooleanField(blank=False, null=False, default=False)

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Full Source Identification (City, Archive, Shelf-mark)",
    )
    # the siglum field as implemented on the old Cantus is composed of both the RISM siglum and the shelfmark
    # it is a human-readable ID for a source
    siglum = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text="RISM-style siglum + Shelf-mark (e.g. GB-Ob 202).",
    )
    holding_institution = models.ForeignKey(
        "Institution",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    shelfmark = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text=(
            "Primary Cantus Database identifier for the source "
            "(e.g. library shelfmark, DACT ID, etc.)"
        ),
        default="[No Shelfmark]",
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="A colloquial or commonly-used name for the source",
    )
    provenance = models.ForeignKey(
        "Provenance",
        on_delete=models.PROTECT,
        help_text="If the origin is unknown, select a location where the source was "
        "used later in its lifetime and provide details in the "
        '"Provenance notes" field.',
        null=True,
        blank=True,
        related_name="sources",
    )
    provenance_notes = models.TextField(
        blank=True,
        null=True,
        help_text="More exact indication of the provenance (if necessary)",
    )

    class SourceCompletenessChoices(models.IntegerChoices):
        FULL_SOURCE = 1, "Complete source"
        FRAGMENT = 2, "Fragment"
        RECONSTRUCTION = 3, "Reconstruction"

    source_completeness = models.IntegerField(
        choices=SourceCompletenessChoices.choices,
        default=SourceCompletenessChoices.FULL_SOURCE,
        verbose_name="Complete Source/Fragment",
    )

    full_source = models.BooleanField(blank=True, null=True)
    date = models.CharField(
        blank=True,
        null=True,
        max_length=63,
        help_text='Date of the source, if known (e.g. "1541")',
    )
    century = models.ManyToManyField("Century", related_name="sources", blank=True)
    notation = models.ManyToManyField("Notation", related_name="sources", blank=True)
    cursus = models.CharField(
        blank=True, null=True, choices=cursus_choices, max_length=63
    )
    current_editors = models.ManyToManyField(
        get_user_model(), related_name="sources_user_can_edit", blank=True
    )

    ######
    # The following five fields have nothing to do with user permissions,
    # instead they give credit to users who are indexers and are displayed
    # on the user detail page as sources the user has contributed to.
    inventoried_by = models.ManyToManyField(
        get_user_model(), related_name="inventoried_sources", blank=True
    )
    full_text_entered_by = models.ManyToManyField(
        get_user_model(), related_name="entered_full_text_for_sources", blank=True
    )
    melodies_entered_by = models.ManyToManyField(
        get_user_model(), related_name="entered_melody_for_sources", blank=True
    )
    proofreaders = models.ManyToManyField(
        get_user_model(), related_name="proofread_sources", blank=True
    )
    other_editors = models.ManyToManyField(
        get_user_model(), related_name="edited_sources", blank=True
    )
    ######

    segment = models.ForeignKey(
        "Segment", on_delete=models.PROTECT, blank=True, null=True
    )
    segment_m2m = models.ManyToManyField(
        "Segment", blank=True, related_name="sources", verbose_name="Segments"
    )
    source_status = models.CharField(
        blank=True, null=True, choices=source_status_choices, max_length=255
    )
    complete_inventory = models.BooleanField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    liturgical_occasions = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    selected_bibliography = models.TextField(blank=True, null=True)
    image_link = models.URLField(
        blank=True,
        null=True,
        help_text="HTTP link to the image gallery of the source.",
    )
    indexing_notes = models.TextField(blank=True, null=True)
    indexing_date = models.TextField(blank=True, null=True)
    json_info = models.JSONField(blank=True, null=True)
    fragmentarium_id = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="fragmentarium ID"
    )
    dact_id = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="DACT ID"
    )
    exists_on_cantus_ultimus = models.BooleanField(
        blank=False, null=False, default=False
    )

    class ProductionMethodChoices(models.IntegerChoices):
        MANUSCRIPT = 1, "Manuscript"
        PRINTED = 2, "Printed"

    production_method = models.IntegerField(
        default=ProductionMethodChoices.MANUSCRIPT,
        choices=ProductionMethodChoices.choices,
        verbose_name="Manuscript/Printed",
    )

    # number_of_chants and number_of_melodies are used for rendering the source-list page (perhaps among other places)
    # they are automatically recalculated in main_app.signals.update_source_chant_count and
    # main_app.signals.update_source_melody_count every time a chant or sequence is saved or deleted
    number_of_chants = models.IntegerField(blank=True, null=True)
    number_of_melodies = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.heading

    def save(self, *args, **kwargs):
        # when creating a source, assign it to "CANTUS Database" segment by default
        if not self.segment:
            cantus_db_segment = Segment.objects.get(name="CANTUS Database")
            self.segment = cantus_db_segment
        super().save(*args, **kwargs)

    @property
    def heading(self) -> str:
        title = []
        if holdinst := self.holding_institution:
            city = f"{holdinst.city}," if holdinst.city else ""
            title.append(city)
            title.append(f"{holdinst.name},")
        else:
            title.append("Cantus")

        title.append(self.shelfmark)

        if self.source_completeness == self.SourceCompletenessChoices.FRAGMENT:
            title.append("(fragment)")

        if self.name:
            title.append(f'("{self.name}")')

        return " ".join(title)

    @property
    def short_heading(self) -> str:
        title = []
        if holdinst := self.holding_institution:
            if holdinst.siglum and holdinst.siglum != "XX-NN":
                title.append(f"{holdinst.siglum}")
            else:
                title.append("Cantus")
        else:
            title.append("Cantus")

        title.append(self.shelfmark)

        if self.source_completeness == self.SourceCompletenessChoices.FRAGMENT:
            title.append("(fragment)")

        return " ".join(title)
