# Generated by Django 4.1.6 on 2024-06-06 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_app", "0013_institution"),
    ]

    operations = [
        migrations.CreateModel(
            name="InstitutionIdentifier",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, help_text="The date this entry was created"
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(
                        auto_now=True, help_text="The date this entry was updated"
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        help_text="Do not provide the full URL here; only the identifier.",
                        max_length=512,
                    ),
                ),
                (
                    "identifier_type",
                    models.IntegerField(
                        choices=[
                            (1, "RISM Online"),
                            (2, "VIAF"),
                            (3, "Wikidata"),
                            (4, "GND (Gemeinsame Normdatei)"),
                            (5, "Bibliothèque national de France"),
                            (6, "Library of Congress"),
                        ]
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="identifiers",
                        to="main_app.institution",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_last_updated_by_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
