# Generated by Django 4.2.5 on 2023-10-20 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cabintypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=14)),
                ('passport_number', models.CharField(max_length=9)),
                ('passport_country_id', models.IntegerField()),
                ('booking_reference', models.CharField(max_length=6)),
                ('confirmed', models.BooleanField(default=False)),
                ('cabin_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cabintypes.cabintype')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.schedule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
