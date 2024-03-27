# Generated by Django 5.0.3 on 2024-03-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
    ]
