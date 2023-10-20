# Generated by Django 4.2.5 on 2023-10-20 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aircrafts', '0001_initial'),
        ('airoutes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('Time', models.TimeField()),
                ('EconomyPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Confirmed', models.BooleanField()),
                ('FlightNumber', models.CharField(blank=True, max_length=10, null=True)),
                ('Aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aircrafts.aircraft')),
                ('Route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airoutes.route')),
            ],
        ),
    ]