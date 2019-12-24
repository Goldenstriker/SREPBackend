from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	is_online = models.BooleanField(default=False)
	

@receiver(user_logged_in, sender = User)
def user_profile_logged_in(sender, user, request, **kwargs):
	print("singal working")
	profile = UserProfile.objects.get(user = user)
	profile.is_online = "True"
	profile.save()


@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user = instance)

@receiver(post_save, sender = User)		
def save_user_profile(sender, instance, **kwargs):
	instance.userprofile.save()
	
# Create your models here.
class Country(models.Model):
  Country_ID=models.AutoField(auto_created=True,primary_key=True,serialize=False)
  Name=models.CharField(max_length=255)
  class Meta:
    db_table="Country"

class State(models.Model):
  State_ID = models.AutoField(auto_created=True,primary_key=True,serialize=False)
  Name = models.CharField(max_length=255)
  Country = models.ForeignKey(Country,on_delete=models.PROTECT)
  class Meta:
    db_table="State"

class City(models.Model):
  City_ID = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
  Name = models.CharField(max_length=255)
  Country = models.ForeignKey(Country,on_delete=models.PROTECT)
  State = models.ForeignKey(State,on_delete=models.PROTECT)
  class Meta:
    db_table="City"

class PropertyType(models.Model):
  ID = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
  Name = models.CharField(max_length=255)
  class Meta:
    db_table="PropertyType"

class PropertyStatus(models.Model):
  ID = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
  Name = models.CharField(max_length=255)
  class Meta:
    db_table="PropertyStatus"
	
class Property(models.Model):
  ID = models.AutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")
  Name = models.CharField(max_length=255)
  Country = models.ForeignKey(Country,on_delete=models.PROTECT)
  State = models.ForeignKey(State,on_delete=models.PROTECT)
  City = models.ForeignKey(City,on_delete=models.PROTECT)
  Property_Type=models.ForeignKey(PropertyType,on_delete=models.PROTECT)
  Property_Status=models.ForeignKey(PropertyStatus,on_delete=models.PROTECT)
  No_Of_BedRooms = models.IntegerField(db_column='No_Of_BedRooms')
  No_Of_BathRooms = models.IntegerField(db_column='No_Of_BathRooms')
  No_Of_Floors = models.IntegerField(db_column='No_Of_Floors')
  Description = models.CharField(max_length=500)
  class Meta:
    db_table="Property"