# Generated by Django 3.1.2 on 2020-10-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dataURI', models.TextField()),
                ('userAns', models.PositiveSmallIntegerField()),
                ('modelPredVal', models.PositiveSmallIntegerField()),
                ('allPredProba', models.JSONField()),
                ('resultPred', models.BooleanField()),
                ('dateTime', models.DateField(auto_now=True)),
            ],
        ),
    ]
