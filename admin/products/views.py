from django.shortcuts import render
from .models import Product, User
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
import random
from .producer import publish
# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all().order_by('id')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product created',  serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk = None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def update(self, request, pk = None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product updated',  serializer.data)

        return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk = None):
        product = Product.objects.get(id=pk)
        product.delete()           
        publish('product deleted',  pk)
        return Response(status = status.HTTP_204_NO_CONTENT)


class UserApiView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id':user.id
        })