# Generated by Django 5.0.3 on 2024-03-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'about',
                'managed': False,
            },
        ),
    ]
