# Generated by Django 4.2.14 on 2024-07-29 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_rename_task_emotion_tasks_emotion_after_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='emotion_after',
            new_name='changed_emotion',
        ),
        migrations.RenameField(
            model_name='tasks',
            old_name='emotion_before',
            new_name='current_emotion',
        ),
    ]
