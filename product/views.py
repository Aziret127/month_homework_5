from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import (
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWithReviewsSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer,
)
from rest_framework import status
from django.db.models import Avg

#Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            data={'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.title = request.data.get('title', product.title)
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.save()
        data = ProductDetailSerializer(product, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

@api_view(['GET', 'POST'])
def product_list_api_view(request):     
    products = Product.objects.all()
    product_id = request.query_params.get('id')
    if product_id:
        products = products.filter(id=product_id)
        data = ProductListSerializer(products, many=True).data
        return Response(
                data=data,
                status=status.HTTP_200_OK
            )
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        product.save()
        return Response(status=status.HTTP_201_CREATED)
    data = ProductListSerializer(products, many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.all().annotate(rating=Avg('reviews__stars'))
    product_id = request.query_params.get('id')
    if product_id:
        products = products.filter(id=product_id)
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    category = Category.objects.all()
    category_id = request.query_params.get('id')
    if category_id:
        category = category.filter(id=category_id)
        data = CategoryListSerializer(category, many=True).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED)
    data = CategoryListSerializer(category, many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )
@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, pk):
    try:
        product = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            data={'error': 'Category not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        data = CategoryDetailSerializer(product, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
            )
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.name = request.data.get('name', product.name)
        product.save()
        data = CategoryDetailSerializer(product, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
            )
@api_view(['GET', 'POST'])
def review_list_api_view(request):
    review = Review.objects.all()
    review_id = request.query_params.get('id')
    if review_id:
        review = review.filter(id=review_id)
        data = ReviewListSerializer(review, many=True).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
    elif request.method == 'POST':
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        review = Review.objects.create(
            text=text,
            product_id=product_id,
            stars=stars
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    data = ReviewListSerializer(review, many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(
            data={'error': 'Review not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
            )
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        review.text = request.data.get('text', review.text)
        review.stars = request.data.get('stars', review.stars)
        review.save()
        data = ReviewDetailSerializer(review, many=False).data
        return Response(
            data=data,
            status=status.HTTP_200_OK
            )