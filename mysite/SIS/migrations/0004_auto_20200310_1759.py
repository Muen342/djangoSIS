# Generated by Django 3.0.3 on 2020-03-10 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIS', '0003_auto_20200310_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='id',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]
