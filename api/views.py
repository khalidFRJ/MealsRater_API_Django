from django.shortcuts import render
from rest_framework import  viewsets , status
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response 
from django.contrib.auth.models import User


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

@action(detail=True, methods=['post'])
def rate_meal(self, request, pk=None):
    if 'stars' in request.data:
        '''
        Create or update
        '''
        meal = Meal.objects.get(id=pk)
        stars = request.data['stars']
        username = request.data['username']
        user = User.objects.get(username=username)

        try:
            # update
            rating = Rating.objects.get(user=user.id, meal=meal.id)  # specific rate
            rating.stars = stars
            rating.save()
            serializer = RatingSerializer(rating, many=False)
            json = {
                'message': 'Meal Rate Updated',
                'result': serializer.data
            }
            return Response(json, status=status.HTTP_200_OK)

        except:
            # create if the rate does not exist
            rating = Rating.objects.create(stars=stars, meal=meal, user=user)
            serializer = RatingSerializer(rating, many=False)
            json = {
                'message': 'Meal Rate Created',
                'result': serializer.data
            }
            return Response(json, status=status.HTTP_200_OK)
    
    else:
        json = {
            'message': 'Stars not provided'
        }
        return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


