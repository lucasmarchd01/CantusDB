# Generated by Django 4.2.3 on 2023-10-09 18:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0008_differentia_chant_differentiae_database_new_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chant",
            name="differentiae_database",
        ),
        migrations.RenameField(
            model_name="chant",
            old_name="differentiae_database_new",
            new_name="differentiae_database",
        ),
        migrations.RemoveField(
            model_name="sequence",
            name="differentiae_database",
        ),
        migrations.RenameField(
            model_name="sequence",
            old_name="differentiae_database_new",
            new_name="differentiae_database",
        ),
    ]
