# Generated by Django 3.2.16 on 2023-01-19 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceEmployee', '0013_percentageattendanceemployee_total_employee_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceemployee',
            name='months',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendanceemployee',
            name='years',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]