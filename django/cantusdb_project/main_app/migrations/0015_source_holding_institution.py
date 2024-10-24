# Generated by Django 4.2.11 on 2024-06-06 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0014_institutionidentifier"),
    ]

    operations = [
        migrations.AddField(
            model_name="source",
            name="holding_institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="main_app.institution",
            ),
        ),
    ]
