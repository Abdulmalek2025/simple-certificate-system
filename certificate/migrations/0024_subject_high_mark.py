# Generated by Django 4.0.4 on 2022-06-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0023_alter_student_current_level_alter_student_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='high_mark',
            field=models.FloatField(blank=True, null=True, verbose_name='الدرجة النهائية'),
        ),
    ]
