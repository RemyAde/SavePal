# Generated by Django 4.1.1 on 2022-10-10 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("savings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="piggy",
            name="miscellaneous",
            field=models.FloatField(blank=True, null=True),
        ),
    ]