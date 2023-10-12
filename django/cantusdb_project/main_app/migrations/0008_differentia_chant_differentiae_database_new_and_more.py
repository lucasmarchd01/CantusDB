# Generated by Django 4.2.3 on 2023-10-05 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "main_app",
            "0007_rename_differentia_new_chant_differentiae_database_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Differentia",
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
                ("differentia_id", models.CharField(max_length=255)),
                (
                    "melodic_transcription",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("mode", models.CharField(blank=True, max_length=255, null=True)),
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
            name="differentiae_database_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="main_app.differentia",
                verbose_name="differentiae database",
            ),
        ),
        migrations.AddField(
            model_name="sequence",
            name="differentiae_database_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="main_app.differentia",
                verbose_name="differentiae database",
            ),
        ),
    ]