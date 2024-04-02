# Generated by Django 5.0.3 on 2024-04-02 09:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.TextField(default='default.jpg')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'about',
                'ordering': ['created'],
                'managed': True,
            },
        ),
    ]
