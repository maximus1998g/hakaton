# Generated by Django 3.1.2 on 2020-10-24 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_city'),
        ('token_auth', '0004_auto_20201023_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.specialization'),
        ),
    ]