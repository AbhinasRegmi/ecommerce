# Generated by Django 4.1.3 on 2022-11-22 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_order_key_order_intent_order_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='intent',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='secret',
            field=models.CharField(max_length=255),
        ),
    ]
