# Generated by Django 3.2.16 on 2023-04-03 07:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('submisssion', '0005_alter_submission_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
