# Generated by Django 5.0.2 on 2024-03-06 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelreg',
            name='bot_btn',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
