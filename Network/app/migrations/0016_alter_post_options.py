# Generated by Django 4.2.4 on 2023-08-20 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
    ]
