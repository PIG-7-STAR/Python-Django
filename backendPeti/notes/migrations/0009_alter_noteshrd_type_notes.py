# Generated by Django 3.2.16 on 2023-02-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_noteshrd_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noteshrd',
            name='type_notes',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]