from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from .serializers import  ProductDetailSerializer, ProductListSerializer, CategoryDetailSerializer, CategoryListSerializer, ReviewListSerializer, ReviewDetailSerializer
from rest_framework import status

#Create your views here.
@api_view(['GET'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            data={'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = ProductDetailSerializer(product, many=False).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
        )

@api_view(['GET'])
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

@api_view(['GET'])
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

@api_view(['GET'])
def category_detail_api_view(request, pk):
    try:
        product = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(
            data={'error': 'Category not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = CategoryDetailSerializer(product, many=False).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
        )

@api_view(['GET'])
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

@api_view(['GET'])
def review_detail_api_view(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(
            data={'error': 'Review not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = ReviewDetailSerializer(review, many=False).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
        )