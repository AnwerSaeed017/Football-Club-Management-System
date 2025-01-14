# Generated by Django 4.2.6 on 2023-12-05 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_date', models.DateField()),
                ('match_occurred', models.BooleanField(default=False)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='clubs.footballclub')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_matches', to='clubs.footballclub')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.league')),
            ],
            options={
                'ordering': ['match_date'],
                'unique_together': {('league', 'home_team', 'away_team', 'match_date')},
            },
        ),
    ]
