# Generated by Django 3.0.3 on 2020-03-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIS', '0008_auto_20200312_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('S', 'Student'), ('T', 'Teacher'), ('M', 'Management'), ('P', 'Parent')], default='S', help_text='Type', max_length=1),
        ),
    ]
