# Generated by Django 3.2.3 on 2021-05-28 11:08

from django.db import migrations, models # type: ignore
import django.db.models.deletion # type: ignore


class Migration(migrations.Migration):

    dependencies = [
        ('research_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_for_die', models.FloatField()),
                ('p_for_reproduction', models.FloatField()),
                ('max_lifetime', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='individual',
            name='parameters',
        ),
        migrations.AddField(
            model_name='individual',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='individual',
            name='is_alive',
            field=models.BooleanField(default=None),
        ),
        migrations.AddField(
            model_name='individual',
            name='type',
            field=models.CharField(choices=[('b', 'bacteria')], default=None, max_length=20),
        ),
        migrations.RemoveField(
            model_name='population',
            name='individuals',
        ),
        migrations.AddField(
            model_name='population',
            name='individuals',
            field=models.ManyToManyField(to='research_app.Individual'),
        ),
        migrations.AddField(
            model_name='individual',
            name='genome',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='research_app.genome'),
        ),
    ]
