# Generated by Django 4.2 on 2023-05-24 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0002_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]
