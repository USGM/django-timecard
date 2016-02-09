# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Upcoming'), (100, b'Paid')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'date',
                'ordering': ('-date', '-start_time'),
                'verbose_name_plural': 'entries',
                'db_table': 'timecard_entries',
                'verbose_name': 'entry',
                'permissions': (('review_entries', 'Can review entries'),),
            },
        ),
    ]
