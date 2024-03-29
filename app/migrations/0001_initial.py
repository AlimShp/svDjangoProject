# Generated by Django 5.0.2 on 2024-03-06 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('user_session', models.CharField(max_length=48)),
                ('user_image', models.CharField(max_length=260, null=True)),
                ('bot_btn', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', models.ImageField(upload_to='app/static/img', verbose_name='Ваше фото')),
            ],
        ),
    ]
