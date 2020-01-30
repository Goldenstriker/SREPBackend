from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import response
from django.contrib.auth.models import User, Group
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, filters, generics 
from .models import UserProfile, Country
import pickle, sklearn, pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def index(request):
	#userlist = User.objects.all().select_related('userprofile')
	res = ""
	userlist = User.objects.all().select_related('userprofile')
	#res = u.userprofile.is_online
	for user in userlist:
		print(user.userprofile.is_online)
		#res = res + user.first_name
	return HttpResponse("First Web Response"+ res)

# Create your views here.


# Create your views here.
def home(request):
    return render(request, 'main/index.html')

from django.shortcuts import render
from django.http import response

# Create your views here.
def home(request):
    return render(request, 'main/index.html')

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class RegisterUserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = CreateUserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    serializer = ""
    try:
        userProfile = UserProfile.objects.get(user = user)
        serializer = UserProfileSerializer(userProfile)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'user':user.username, 'user_id': user.id,"userprofile":serializer.data })
	
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def set_user_status(request,userid):
    try:
        userProfile = UserProfile.objects.get(user = userid)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserProfileStatusSerializer(userProfile,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_404_NOT_FOUND)
	
class CountryViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = Country.objects.all()
	serializer_class = CountrySerializer
	
class StateViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = State.objects.all()
	serializer_class = StateSerializer

class CityViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = City.objects.all()
	serializer_class = CitySerializer
	
class PropertyViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = Property.objects.all()
	serializer_class = PropertySerializer

class PropertyTypeViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = PropertyType.objects.all()
	serializer_class = PropertyTypeSerializer

class PropertyStatusViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = PropertyStatus.objects.all()
	serializer_class = PropertyStatusSerializer

class PropertyPurposeViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = PropertyPurpose.objects.all()
	serializer_class = PropertyPurposeSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def recommend(request):
  data = pd.DataFrame(Property.objects.values('Address', 'AreaSqFt', 'City', 'Country',  'Description', 'ID', 'Name', 'No_Of_BathRooms', 'No_Of_BedRooms', 'No_Of_Floors', 'No_Of_LivingRooms', 'Price', 'Property_Purpose__Name', 'Property_Status__Name', 'Property_Type__Name', 'State', 'UserCreatedBy', 'UserCreatedDate'))
  data["Combination"] = data.astype(str).apply(' '.join, axis=1)
  print(data["Combination"])
  cv = CountVectorizer()
  count_matrix = cv.fit_transform(data['Combination'])
  # creating a similarity score matrix
  sim = cosine_similarity(count_matrix)
  # getting the index of the movie in the dataframe
  i = data.loc[data.Combination.str.contains('Mumbai',case=False)].index[0]

  # fetching the row containing similarity scores of the movie
  # from similarity matrix and enumerate it
  lst = list(enumerate(sim[i]))

  # sorting this list in decreasing order based on the similarity score
  lst = sorted(lst, key = lambda x:x[1] ,reverse=True)

  # taking top 1- movie scores
  # not taking the first index since it is the same movie
  lst = lst[1:11]

  # making an empty list that will containg all 10 movie recommendations
  l = []
  for i in range(len(lst)):
      a = lst[i][0]
      l.append(data['Name'][a])
  return JsonResponse(l,safe=False)

class PropertyFilterViewSet(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['UserCreatedBy__id', 'Name','Description','Address','City__Name','State__Name','Price','Property_Purpose__Name']

class PropertyBasedOnUserViewSet(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['UserCreatedBy__id']


class UserProfileViewSet(viewsets.ModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  lookup_field = 'user'

def predictSalePrice(request):
  file = open("dataproviderapp/trainedmodels/sale_price_prediction.pkl",'rb')
  model = pickle.load(file)
  print(model.predict([[1.921320e+03, 6.000000e+00, 4.000000e+00, 2.000000e+00,
            2.000000e+00]]))
  return JsonResponse({'user': model.predict([[1.921320e+03, 6.000000e+00, 4.000000e+00, 2.000000e+00,
            2.000000e+00]])[0]})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chartdata(request):
  data = pd.DataFrame(Property.objects.values('Address', 'AreaSqFt', 'City__Name', 'Country',  'Description', 'ID', 'Name', 'No_Of_BathRooms', 'No_Of_BedRooms', 'No_Of_Floors', 'No_Of_LivingRooms', 'Price', 'Property_Purpose__Name', 'Property_Status__Name', 'Property_Type__Name', 'State', 'UserCreatedBy', 'UserCreatedDate'))
  city_count = data["City__Name"].value_counts()
  property_purpose = data["Property_Purpose__Name"].value_counts()
  property_type= data["Property_Type__Name"].value_counts()
  property_status = data["Property_Status__Name"].value_counts()
  return JsonResponse({"property_type":property_type.to_json(),"property_purpose": property_purpose.to_json(),"property_status":property_status.to_json(),"city_count":city_count.to_json()},safe=False)