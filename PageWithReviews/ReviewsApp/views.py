from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector

from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.template import RequestContext

# Create your views here.

from .models import Review
from .serializers import ReviewSerializer

def index(request):
    reviews = Review.objects.order_by('-id')

    context = {'reviews': reviews}

    return render(
        request,
        'ReviewsApp/index.html',
        context
    )

def answer_me(request):
    """ Сортировка и поиск соответствующих отзывов"""

    inputRequest = request.GET.get('inputRequest')

    inputList = inputRequest.split(" ")
    searchValue = ''
    sortValue = ''

    if "search" in inputList:
        searchValue = request.GET.get('searchValue')

    if "sort" in inputList:
        sortValue = request.GET.get('sortValue')

    if sortValue == '':
        reviews = Review.objects.order_by('-id').annotate(
            search=SearchVector('content', 'rating', 'blogger__first_name', 'blogger__last_name'),
        ).filter(search__icontains=searchValue)
    else:
        reviews = Review.objects.order_by(sortValue, '-id').annotate(
            search=SearchVector('content', 'rating', 'blogger__first_name', 'blogger__last_name'),
        ).filter(search__icontains=searchValue)

    serializer = ReviewSerializer(reviews, many=True)

    context = {'reviews': serializer.data}

    return JsonResponse(context)

@csrf_exempt
def reviews_api(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects;
        serializer = ReviewSerializer(reviews, many=True)
        return Response({"reviews": serializer.data})
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save();
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)