from apps.category.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from django.db import models


class CategoriesView(APIView):
    def get(self, request, format=None):
        if Category.objects.all().exists():
            categories = Category.objects.all()

            result = []

            for category in categories:
                if not category.parent:
                    item = {}
                    item['id'] = category.id
                    item['name'] = category.name
                    item['description'] = category.description
                    item['thumbnail'] = category.thumbnail.url if category.thumbnail else ''

                    item['sub_categories'] = []

                    for cat in categories:
                        sub_item = {}
                        if cat.parent and cat.parent.id == category.id:
                            sub_item['id'] = cat.id
                            sub_item['name'] = cat.name
                            sub_item['description'] = cat.description
                            sub_item['thumbnail'] = cat.thumbnail.url if cat.thumbnail else ''

                            item['sub_categories'].append(sub_item)

                    result.append(item)

            return Response({'categories': result}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No categories found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        name = request.data.get('name')
        description = request.data.get('description')
        if not name or not description:
            return Response({'error': 'Name and description are required'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data={
            'name': name,
            'description': description,
        })
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
