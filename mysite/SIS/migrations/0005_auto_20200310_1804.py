# Generated by Django 3.0.3 on 2020-03-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIS', '0004_auto_20200310_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
