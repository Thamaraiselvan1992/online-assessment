# Generated by Django 4.0.3 on 2022-04-12 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_projects', '0002_remove_bug_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]