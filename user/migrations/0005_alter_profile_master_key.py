# Generated by Django 3.2.3 on 2021-06-11 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_master_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='master_key',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
