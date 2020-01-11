from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import *
# Register your models here.
#admin.site.register(UserProfile)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display=("user","is_online",)
	ordering = ("user",)
	search_fields = ("user",)


#admin.site.register(Country)
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
	list_display=("Country_ID","Name",)
	ordering = ("Country_ID","Name",)
	search_fields = ("Country_ID","Name",)


#admin.site.register(State)
class CustomModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		if (isinstance(obj, User)):
			return "%s" % (obj.username)
		return "%s" % (obj.Name)

class CustomStateAdminForm(forms.ModelForm):
	Country = CustomModelChoiceField(queryset=Country.objects.all()) 
	class Meta:
		model = State
		fields = ['State_ID', 'Name',]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	list_display=("State_ID","Name","Country__Name")
	ordering = ("State_ID","Name",)
	search_fields = ("State_ID","Name","Country__Name")
	form = CustomStateAdminForm
	def Country__Name(self, instance):
		return instance.Country.Name



class CustomCityAdminForm(forms.ModelForm):
	Country = CustomModelChoiceField(queryset=Country.objects.all()) 
	State = CustomModelChoiceField(queryset=State.objects.all())
	class Meta:
		model = City
		fields = ['City_ID', 'Name',]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
	list_display=("City_ID","Name","State__Name","Country__Name")
	ordering = ("City_ID","Name","State__Name","Country__Name")
	search_fields = ("State_ID","Name","State__Name","Country__Name")
	form = CustomCityAdminForm
	def Country__Name(self, instance):
		return instance.Country.Name
	def State__Name(self, instance):
		return instance.State.Name

#admin.site.register(City)
@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
	list_display=("Name",)
	ordering = ("Name",)
	search_fields = ("Name",)
	

@admin.register(PropertyStatus)
class PropertyStatusAdmin(admin.ModelAdmin):
	list_display=("Name",)
	ordering = ("Name",)
	search_fields = ("Name",)

#PropertyPurpose
@admin.register(PropertyPurpose)
class PropertyPurposeAdmin(admin.ModelAdmin):
	list_display=("Name",)
	ordering = ("Name",)
	search_fields = ("Name",)
	
class CustomPropertyAdminForm(forms.ModelForm):
	Country = CustomModelChoiceField(queryset=Country.objects.all()) 
	State = CustomModelChoiceField(queryset=State.objects.all())
	City = CustomModelChoiceField(queryset=City.objects.all())
	Property_Type = CustomModelChoiceField(queryset=PropertyType.objects.all())
	Property_Status = CustomModelChoiceField(queryset=PropertyStatus.objects.all())
	Property_Purpose = CustomModelChoiceField(queryset=PropertyPurpose.objects.all())
	UserCreatedBy = CustomModelChoiceField(queryset=User.objects.all())
	class Meta:
		model = Property
		fields = ["Name","Description","Address",
					"No_Of_BedRooms",
					"No_Of_LivingRooms",
					"No_Of_BathRooms","No_Of_Floors",
					"AreaSqFt","Price", "UserCreatedDate"]

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
	list_display=("ID","Name","Description","Address",
					"No_Of_BedRooms",
					"No_Of_LivingRooms",
					"No_Of_BathRooms","No_Of_Floors","Country__Name",
					"State__Name","City__Name","PropertyStatus__Name","PropertyType__Name",
					"AreaSqFt","Price", "UserCreatedBy","UserCreatedDate")
	ordering = ("Name",)
	search_fields = ("Name",)
	form = CustomPropertyAdminForm
	def Country__Name(self, instance):
		return instance.Country.Name
	def State__Name(self, instance):
		return instance.State.Name
	def City__Name(self, instance):
		return instance.City.Name	
	def PropertyStatus__Name(self, instance):
		return instance.Property_Status.Name
	def PropertyType__Name(self, instance):
		return instance.Property_Type.Name