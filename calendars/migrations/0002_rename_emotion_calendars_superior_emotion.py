# Generated by Django 4.2.14 on 2024-08-02 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendars',
            old_name='emotion',
            new_name='superior_emotion',
        ),
    ]
