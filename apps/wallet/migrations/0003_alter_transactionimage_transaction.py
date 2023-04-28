# Generated by Django 4.2 on 2023-04-26 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_rename_image_transactionimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionimage',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='wallet.transaction'),
        ),
    ]
