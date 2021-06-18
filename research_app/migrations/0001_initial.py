# Generated by Django 3.2.1 on 2021-05-13 13:52

from django.db import migrations, models  # type: ignore
import django.utils.timezone  # type: ignore
import jsonfield.fields  # type: ignore


class Migration(migrations.Migration):

    initial = True

    dependencies: list = [
    ]

    operations = [
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameters', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('population_id', models.IntegerField()),
                ('parameters', jsonfield.fields.JSONField()),
                ('result', jsonfield.fields.JSONField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('individuals', jsonfield.fields.JSONField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
