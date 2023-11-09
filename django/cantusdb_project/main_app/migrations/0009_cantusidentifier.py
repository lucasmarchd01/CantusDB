# Generated by Django 4.2.3 on 2023-11-09 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_app", "0008_differentia_chant_diff_db_sequence_diff_db"),
    ]

    operations = [
        migrations.CreateModel(
            name="CantusIdentifier",
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
                ("cantus_id", models.CharField(max_length=255)),
                ("full_text", models.TextField(blank=True, null=True)),
                (
                    "cao_sources",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("cao", models.CharField(blank=True, max_length=255, null=True)),
                ("concordances", models.JSONField(blank=True, null=True)),
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
                    "genre",
                    models.ManyToManyField(
                        blank=True,
                        related_name="cantus_identifiers",
                        to="main_app.genre",
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