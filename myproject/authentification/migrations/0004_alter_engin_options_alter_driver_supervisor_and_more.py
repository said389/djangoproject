# Generated by Django 5.2 on 2025-05-11 21:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0003_alter_driver_supervisor_alter_engin_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='engin',
            options={},
        ),
        migrations.AlterField(
            model_name='driver',
            name='supervisor',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'ChefEscale'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conducteurs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='engin',
            table='engin',
        ),
    ]
