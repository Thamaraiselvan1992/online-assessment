# Generated by Django 4.0.4 on 2022-04-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_projects', '0011_remove_projectmodule_assign_module_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='project_module',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
