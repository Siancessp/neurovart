# Generated by Django 5.0.7 on 2024-07-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neurovart', '0003_payments_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet_transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_id', models.IntegerField()),
                ('transaction_id', models.IntegerField(blank=True, null=True)),
                ('opening', models.DecimalField(decimal_places=5, default=0, max_digits=15)),
                ('credit', models.DecimalField(decimal_places=5, default=0, max_digits=15)),
                ('debit', models.DecimalField(decimal_places=5, default=0, max_digits=15)),
                ('closing', models.DecimalField(decimal_places=5, default=0, max_digits=15)),
                ('message', models.CharField(blank=True, max_length=155, null=True)),
                ('from_to', models.IntegerField(blank=True, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'wallet_transactions',
            },
        ),
    ]
