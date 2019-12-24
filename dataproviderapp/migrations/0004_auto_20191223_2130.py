# Generated by Django 2.1.12 on 2019-12-24 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataproviderapp', '0003_auto_20191223_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('ID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('No_Of_BedRooms', models.IntegerField(db_column='No_Of_BedRooms')),
                ('No_Of_BathRooms', models.IntegerField(db_column='No_Of_BathRooms')),
                ('No_Of_Floors', models.IntegerField(db_column='No_Of_Floors')),
                ('Description', models.CharField(max_length=500)),
                ('City', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataproviderapp.City')),
                ('Country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataproviderapp.Country')),
                ('Property_Status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataproviderapp.PropertyStatus')),
                ('Property_Type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataproviderapp.PropertyType')),
            ],
            options={
                'db_table': 'Property',
            },
        ),
        migrations.RenameField(
            model_name='state',
            old_name='FK_Country_ID',
            new_name='Country',
        ),
        migrations.AddField(
            model_name='property',
            name='State',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataproviderapp.State'),
        ),
    ]