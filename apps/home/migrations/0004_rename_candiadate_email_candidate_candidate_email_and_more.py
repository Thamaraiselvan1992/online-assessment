# Generated by Django 4.0.3 on 2022-04-06 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps_home', '0003_candidate_candidateassessment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='candiadate_email',
            new_name='candidate_email',
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='candiadate_mobile',
            new_name='candidate_mobile',
        ),
        migrations.RenameField(
            model_name='candidate',
            old_name='candiadate_name',
            new_name='candidate_name',
        ),
        migrations.RenameField(
            model_name='candidateassessment',
            old_name='candiadate_id',
            new_name='candidate_id',
        ),
    ]
