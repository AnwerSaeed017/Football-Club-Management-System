# Generated by Django 4.2.6 on 2023-12-05 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClubDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stadium_name', models.CharField(max_length=100)),
                ('stadium_capacity', models.PositiveIntegerField()),
                ('stadium_location', models.CharField(max_length=200)),
                ('stadium_opened_year', models.PositiveIntegerField()),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clubs.footballclub')),
            ],
        ),
    ]