# Generated by Django 3.2.16 on 2023-02-03 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0023_remove_user_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee_code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]