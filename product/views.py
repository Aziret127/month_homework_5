from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Product, Category, Review
from .serializers import (
    ProductListSerializer,
    ProductValidateSerializer,
    CategoryListSerializer,
    CategoryValidateSerializer,
    ReviewListSerializer,
    ReviewValidateSerializer,
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryValidateSerializer
        return CategoryListSerializer

class ProductViewSet(viewsets.ModelViewSet):
   
    queryset = Product.objects.select_related().all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductValidateSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('id')
        if product_id:
            queryset = queryset.filter(id=product_id)
        return queryset

    @action(detail=False, methods=['get'])
    def reviews(self, request):
        """
        Эндпоинт: /api/products/reviews/
        Выводит продукты с аннотацией среднего рейтинга
        """
        products = self.get_queryset().annotate(rating=Avg('reviews__stars'))
        serializer = self.get_serializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewValidateSerializer
        return ReviewListSerializer









# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product, Category, Review
# from .serializers import (
#     ProductDetailSerializer,
#     ProductListSerializer,
#     ProductWithReviewsSerializer,
#     ProductValidateSerializer,
#     CategoryDetailSerializer,
#     CategoryListSerializer,
#     CategoryValidateSerializer,
#     ReviewListSerializer,
#     ReviewDetailSerializer,
#     ReviewValidateSerializer,
# )
# from rest_framework import status
# from django.db.models import Avg
# from rest_framework.viewsets import ModelViewSet
# #Create your views here.
# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.select_for_update('category').all()
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return ProductListSerializer
#         elif self.action == 'retrieve':
#             return ProductDetailSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return ProductValidateSerializer
#         return ProductDetailSerializer
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(
#             data={'error': 'Product not found'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     if request.method == 'GET':
#         data = ProductDetailSerializer(product, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#         )
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         product.title = request.data.get('title', product.title)
#         product.description = request.data.get('description', product.description)
#         product.price = request.data.get('price', product.price)
#         product.save()
#         data = ProductDetailSerializer(product, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#         )

# @api_view(['GET', 'POST'])
# def product_list_api_view(request):     
#     products = Product.objects.all()
#     product_id = request.query_params.get('id')
#     if product_id:
#         products = products.filter(id=product_id)
#         data = ProductListSerializer(products, many=True).data
#         return Response(
#                 data=data,
#                 status=status.HTTP_200_OK
#             )
#     elif request.method == 'POST':
#         validate_serializer = ProductValidateSerializer(data=request.data)
#         if not validate_serializer.is_valid():
#             return Response(
#                 data=validate_serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         title = request.data.get('title')
#         description = request.data.get('description')
#         price = request.data.get('price')
#         category_id = request.data.get('category_id')
#         product = Product.objects.create(
#             title=title,
#             description=description,
#             price=price,
#             category_id=category_id
#         )
#         product.save()
#         return Response(status=status.HTTP_201_CREATED)
#     data = ProductListSerializer(products, many=True).data
#     return Response(
#         data=data,
#         status=status.HTTP_201_CREATED
#     )

# @api_view(['GET'])
# def product_reviews_list_api_view(request):
#     products = Product.objects.all().annotate(rating=Avg('reviews__stars'))
#     product_id = request.query_params.get('id')
#     if product_id:
#         products = products.filter(id=product_id)
#     data = ProductWithReviewsSerializer(products, many=True).data
#     return Response(data=data, status=status.HTTP_200_OK)

# class CategoryViewSet(ModelViewSet):
#     queryset = Category.objects.all()
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return CategoryListSerializer
#         elif self.action == 'retrieve':
#             return CategoryDetailSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return CategoryValidateSerializer
#         return CategoryDetailSerializer


# @api_view(['GET', 'POST'])
# def category_list_api_view(request):
#     category = Category.objects.all()
#     category_id = request.query_params.get('id')
    
#     if category_id:
#         category = category.filter(id=category_id).distinct()
#         data = CategoryListSerializer(category, many=True).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#         )
#     elif request.method == 'POST':
#         validate_serializer = CategoryValidateSerializer(data=request.data)
#         if not validate_serializer.is_valid():
#             return Response(
#                 data=validate_serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         name = request.data.get('name')
#         if Category.objects.filter(name=name).exists():
#             return Response(
#                 data={'error': 'Category with this name already exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         category = Category.objects.create(name=name)
#         return Response(status=status.HTTP_201_CREATED)
#     unique_categories = []
#     seen_names = set()
#     for cat in category.order_by('id'):
#         if cat.name not in seen_names:
#             unique_categories.append(cat)
#             seen_names.add(cat.name)
   
#     data = CategoryListSerializer(unique_categories, many=True).data
#     return Response(
#         data=data,
#         status=status.HTTP_200_OK  
#     )

# def category_list_api_view(request):
#     category = Category.objects.all().distinct()
#     category_id = request.query_params.get('id')
#     if category_id:
#         category = category.filter(id=category_id).distinct()
#         data = CategoryListSerializer(category, many=True).data
#         category = category.distinct()
#         return Response(
#                 data=data,
#                 status=status.HTTP_200_OK
#             )
#     elif request.method == 'POST':
#         validate_serializer = CategoryValidateSerializer(data=request.data)
#         if not validate_serializer.is_valid():
#             return Response(
#                 data=validate_serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         name = request.data.get('name')
#         category = Category.objects.create(name=name)
#         category.save()
#         return Response(status=status.HTTP_201_CREATED)
#     data = CategoryListSerializer(category, many=True).data
#     return Response(
#         data=data,
#         status=status.HTTP_201_CREATED
#     )
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         return Response(
#             data={'error': 'Category not found'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     if request.method == 'GET':
#         data = CategoryDetailSerializer(category, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#             )
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         category.name = request.data.get('name',)
#         category.save()
#         data = CategoryDetailSerializer(category, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#             )


# class ReviewViewSet(ModelViewSet):
#     queryset = Review.objects.all()
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return ReviewListSerializer
#         elif self.action == 'retrieve':
#             return ReviewDetailSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return ReviewValidateSerializer
#         return ReviewDetailSerializer
    

# @api_view(['GET', 'POST'])
# def review_list_api_view(request):
#     review = Review.objects.all()
#     review_id = request.query_params.get('id')
#     if review_id:
#         review = review.filter(id=review_id)
#         data = ReviewListSerializer(review, many=True).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#         )
#     elif request.method == 'POST':
#         validate_serializer = ReviewValidateSerializer(data=request.data)
#         if not validate_serializer.is_valid():
#             return Response(
#                 data=validate_serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         text = request.data.get('text')
#         product_id = request.data.get('product_id')
#         stars = request.data.get('stars')
#         review = Review.objects.create(
#             text=text,
#             product_id=product_id,
#             stars=stars
#         )
#         review.save()
#         return Response(status=status.HTTP_201_CREATED)
#     data = ReviewListSerializer(review, many=True).data
#     return Response(
#         data=data,
#         status=status.HTTP_201_CREATED
#     )
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, pk):
#     try:
#         review = Review.objects.get(pk=pk)
#     except Review.DoesNotExist:
#         return Response(
#             data={'error': 'Review not found'},
#             status=status.HTTP_404_NOT_FOUND
#         )
#     if request.method == 'GET':
#         data = ReviewDetailSerializer(review, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#             )
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         review.text = request.data.get('text', review.text)
#         review.stars = request.data.get('stars', review.stars)
#         review.save()
#         data = ReviewDetailSerializer(review, many=False).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK
#             )