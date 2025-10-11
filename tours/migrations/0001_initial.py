# Generated migration for TourBooking model

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TourBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('preferred_home', models.CharField(choices=[('cardiff', 'Cardiff Bay'), ('barry', 'Barry Seaside'), ('waverley', 'Waverley Centre'), ('college-fields', 'College Fields')], max_length=20)),
                ('preferred_date', models.DateField()),
                ('preferred_time', models.TimeField()),
                ('number_of_visitors', models.PositiveIntegerField(default=1)),
                ('special_requirements', models.TextField(blank=True, null=True)),
                ('care_type_interest', models.CharField(choices=[('residential', 'Residential Care'), ('nursing', 'Nursing Care'), ('dementia', 'Dementia Care'), ('respite', 'Respite Care'), ('general', 'General Inquiry')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('staff_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Tour Booking',
                'verbose_name_plural': 'Tour Bookings',
                'ordering': ['-created_at'],
            },
        ),
    ]