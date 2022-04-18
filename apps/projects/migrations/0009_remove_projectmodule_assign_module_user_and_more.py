# Generated by Django 4.0.4 on 2022-04-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_projects', '0008_remove_projectmodule_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodule',
            name='assign_module_user',
        ),
        migrations.AddField(
            model_name='projectmodule',
            name='assign_module_user',
            field=models.CharField(default=12, max_length=200),
            preserve_default=False,
        ),
    ]
