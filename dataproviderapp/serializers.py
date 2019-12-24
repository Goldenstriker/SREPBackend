from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import UserProfile, Country, State, City, Property

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'is_online']


class UserProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['is_online']


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
		#print(user)
        print(user)
        #UserProfile.objects.create(user=user)
        #user.userprofile.save()
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #userprofile = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    userprofile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name','userprofile')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
		#print(user)
        print(user)
        #userprofile = UserProfile.objects.create(user=user)
        #userprofile.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["Country_ID","Name"]

class StateSerializer(serializers.ModelSerializer):
	Country = CountrySerializer()
	class Meta:
		model = State
		fields = ["State_ID","Name","Country"]

class CitySerializer(serializers.ModelSerializer):
	State = StateSerializer()
	class Meta:
		model = City
		fields = ["City_ID","Name","State"]

class PropertySerializer(serializers.ModelSerializer):
	City = StateSerializer()
	class Meta:
		model = Property
		fields = ["ID","Name","Description","No_Of_BedRooms",
					"No_Of_BathRooms","No_Of_Floors","Country",
					"State","City","Property_Status","Property_Type"]