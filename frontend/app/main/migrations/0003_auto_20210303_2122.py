# Generated by Django 3.1.7 on 2021-03-03 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210303_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceaction',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='deviceaction',
            name='finished_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='devicelog',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
