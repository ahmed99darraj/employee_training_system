# Generated by Django 5.0 on 2024-12-28 20:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='total_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='إجمالي ساعات الدورة'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='تاريخ الحضور')),
                ('is_present', models.BooleanField(default=True, verbose_name='حاضر')),
                ('hours_attended', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='عدد ساعات الحضور')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.course', verbose_name='الدورة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المتدرب')),
            ],
            options={
                'verbose_name': 'سجل الحضور',
                'verbose_name_plural': 'سجلات الحضور',
                'unique_together': {('user', 'course', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True, verbose_name='تاريخ الإصدار')),
                ('total_hours', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='إجمالي الساعات')),
                ('certificate_file', models.FileField(upload_to='certificates/', verbose_name='ملف الشهادة')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.course', verbose_name='الدورة')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المتدرب')),
            ],
            options={
                'verbose_name': 'شهادة',
                'verbose_name_plural': 'الشهادات',
                'unique_together': {('user', 'course')},
            },
        ),
    ]