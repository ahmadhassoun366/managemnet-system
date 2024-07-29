# Generated by Django 5.0.6 on 2024-07-24 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('office_type', models.CharField(choices=[('single', 'Single Office for 1 Person'), ('multiple', 'Office for Multiple Persons'), ('meeting', 'Meeting Room'), ('lab', 'Lab with PCs'), ('suite', 'Private Office Suite'), ('coworking', 'Co-working Space'), ('hotdesk', 'Hot Desk Area'), ('conference', 'Conference Room'), ('studio', 'Creative Studio'), ('training', 'Training Room')], default='single', max_length=15)),
                ('capacity', models.IntegerField()),
                ('amenities', models.TextField()),
                ('location', models.TextField()),
                ('price_per_hour', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.space')),
            ],
        ),
    ]
