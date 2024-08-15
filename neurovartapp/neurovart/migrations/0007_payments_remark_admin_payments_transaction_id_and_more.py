# Generated by Django 5.0.7 on 2024-07-27 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neurovart', '0006_customers_is_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='remark_admin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payouts',
            name='transaction_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]