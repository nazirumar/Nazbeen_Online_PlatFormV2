# Generated by Django 5.1.4 on 2024-12-21 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_embedding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='embedding',
        ),
        migrations.AddField(
            model_name='course',
            name='pinecone_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]