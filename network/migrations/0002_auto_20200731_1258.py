# Generated by Django 2.2.7 on 2020-07-31 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='follows',
            new_name='follow',
        ),
    ]