# Generated by Django 5.0.7 on 2024-07-29 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neurovart', '0010_investmentforfund_applyforfund_cus_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentforfund',
            name='invested_at',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]