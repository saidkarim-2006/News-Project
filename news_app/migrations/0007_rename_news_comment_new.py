# Generated by Django 4.2.2 on 2023-07-29 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='news',
            new_name='new',
        ),
    ]
