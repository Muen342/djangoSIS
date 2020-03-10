# Generated by Django 3.0.3 on 2020-03-10 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIS', '0002_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance',
            field=models.CharField(blank=True, choices=[('A', 'Attendance'), ('P', 'Present'), ('E', 'Excused')], default='P', help_text='Attendance', max_length=1),
        ),
    ]
