# Generated by Django 3.1.2 on 2020-10-24 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0011_auto_20201024_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='external',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='link',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]
