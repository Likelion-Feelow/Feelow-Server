# Generated by Django 4.2.14 on 2024-07-31 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_rename_emotion_after_tasks_changed_emotion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='feedback',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
