# Generated by Django 2.1 on 2019-06-13 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wx_wxb',
            name='wx_url',
            field=models.CharField(max_length=1000, verbose_name='原文链接'),
        ),
    ]