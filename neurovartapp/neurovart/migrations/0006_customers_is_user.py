# Generated by Django 5.0.7 on 2024-07-24 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neurovart', '0005_payouts'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='is_user',
            field=models.IntegerField(default=0),
        ),
    ]