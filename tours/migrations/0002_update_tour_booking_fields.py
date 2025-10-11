# Generated migration for updated TourBooking model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        # Make last_name optional
        migrations.AlterField(
            model_name='tourbooking',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        
        # Remove phone number validation
        migrations.AlterField(
            model_name='tourbooking',
            name='phone_number',
            field=models.CharField(max_length=17),
        ),
        
        # Remove unused fields
        migrations.RemoveField(
            model_name='tourbooking',
            name='number_of_visitors',
        ),
        migrations.RemoveField(
            model_name='tourbooking',
            name='special_requirements',
        ),
        migrations.RemoveField(
            model_name='tourbooking',
            name='care_type_interest',
        ),
        migrations.RemoveField(
            model_name='tourbooking',
            name='is_confirmed',
        ),
        migrations.RemoveField(
            model_name='tourbooking',
            name='staff_notes',
        ),
        
        # Add new fields
        migrations.AddField(
            model_name='tourbooking',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tourbooking',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('visited', 'Visited'), ('not_visited', 'Not Visited')],
                default='pending',
                max_length=20
            ),
        ),
        
        # Update home choices
        migrations.AlterField(
            model_name='tourbooking',
            name='preferred_home',
            field=models.CharField(
                choices=[('cardiff', 'Cardiff'), ('barry', 'Barry'), ('waverley', 'Waverley'), ('college-fields', 'College Fields')],
                max_length=20
            ),
        ),
    ]