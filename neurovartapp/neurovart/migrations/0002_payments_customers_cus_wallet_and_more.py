# Generated by Django 5.0.7 on 2024-07-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neurovart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_id', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gateway', models.CharField(blank=True, default='CRYPTO_GATEWAY', max_length=50, null=True)),
                ('status', models.CharField(default='PENDING', max_length=25)),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.AddField(
            model_name='customers',
            name='cus_wallet',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='customers',
            name='package_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='customers',
            name='purchase_package',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
