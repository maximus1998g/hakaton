# Generated by Django 3.1.2 on 2020-10-24 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0005_auto_20201024_1347'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='formachievements',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='formeducations',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='formextraskills',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='formjobs',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='formsoftskills',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='jobduties',
            unique_together=set(),
        ),
    ]
