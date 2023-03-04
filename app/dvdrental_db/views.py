from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from dvdrental_db.models import Movies
from dvdrental_db.serializers import TutorialSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Movies.objects.all()
    return render(request, "tutorials/index.html", {'tutorials': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tutorials/index.html'

    def get(self, request):
        queryset = Movies.objects.all()
        return Response({'movies': queryset})


class list_all_tutorials(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tutorials/tutorial_list.html'

    def get(self, request):
        queryset = Movies.objects.all()
        return Response({'movies': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        movies = Movies.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            movies = movies.filter(title__icontains=title)

        tutorials_serializer = TutorialSerializer(movies, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Movies.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Tutorials were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try:
        movies = Movies.objects.get(pk=pk)
    except Movies.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(movies)
        return JsonResponse(tutorial_serializer.data)

    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(movies, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movies.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tutorial_list_published(request):
    movies = Movies.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(movies, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)