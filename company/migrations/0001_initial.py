# Generated by Django 3.1.2 on 2020-10-23 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('inn', models.CharField(blank=True, max_length=32)),
                ('ogrn', models.CharField(blank=True, max_length=32)),
                ('city', models.CharField(blank=True, max_length=128)),
                ('address', models.CharField(blank=True, max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=32)),
                ('takes_on_practice', models.BooleanField(blank=True, default=False, max_length=256)),
                ('logo', models.TextField(blank=True)),
                ('hr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'company',
            },
        ),
    ]
