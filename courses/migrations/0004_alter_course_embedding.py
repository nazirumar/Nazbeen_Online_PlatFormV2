# Generated by Django 5.1.4 on 2024-12-21 05:08

import pgvector.django
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_embedding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='embedding',
            field=pgvector.django.VectorField(blank=True, default=None, dimensions=384, null=True),
        ),
    ]
