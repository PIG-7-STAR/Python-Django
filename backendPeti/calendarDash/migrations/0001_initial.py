# Generated by Django 3.2.16 on 2023-01-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarDashHRD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_days', models.CharField(max_length=220, null=True)),
                ('date', models.DateField(null=True)),
                ('years', models.IntegerField(null=True)),
                ('months', models.IntegerField(null=True)),
                ('days', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DashboardHRD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_days', models.CharField(max_length=220, null=True)),
                ('total_employee', models.IntegerField(null=True)),
                ('hour_perday', models.IntegerField(null=True)),
                ('total_hour', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]