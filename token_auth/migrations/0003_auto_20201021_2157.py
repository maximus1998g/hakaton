# Generated by Django 3.1.2 on 2020-10-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_auth', '0002_remove_userprofile_vk_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='course',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='degree',
            field=models.CharField(choices=[('BACHELOR', 'BACHELOR'), ('MASTER', 'MASTER')], default='BACHELOR', max_length=16),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='specialization',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], default='MALE', max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='student_id',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='student_id_type',
            field=models.CharField(choices=[('TAB', 'TAB'), ('DIPLOMA', 'DIPLOMA')], default='DIPLOMA', max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(choices=[('ADMINISTRATOR', 'ADMINISTRATOR'), ('EMPLOYER', 'EMPLOYER'), ('STUDENT', 'STUDENT')], default='STUDENT', max_length=16),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='university_id',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
