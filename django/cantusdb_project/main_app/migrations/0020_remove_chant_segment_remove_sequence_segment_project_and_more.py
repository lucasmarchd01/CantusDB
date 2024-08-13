# Generated by Django 4.2.11 on 2024-06-18 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main_app", "0019_remove_source_rism_siglum_delete_rismsiglum"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chant",
            name="segment",
        ),
        migrations.RemoveField(
            model_name="sequence",
            name="segment",
        ),
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=63)),
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
        migrations.AddField(
            model_name="chant",
            name="project",
            field=models.ForeignKey(
                blank=True,
                help_text="The project this chant belongs to. If left blank,this chant is considered part of the Cantus (default) project.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="main_app.project",
            ),
        ),
        migrations.AddField(
            model_name="sequence",
            name="project",
            field=models.ForeignKey(
                blank=True,
                help_text="The project this chant belongs to. If left blank,this chant is considered part of the Cantus (default) project.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="main_app.project",
            ),
        ),
    ]