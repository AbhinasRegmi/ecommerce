# Generated by Django 4.1.3 on 2022-11-26 07:00

from django.db import migrations, models
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_productimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='product/default.png', upload_to='product/', validators=[store.validators.validate_max_image_size]),
        ),
    ]
