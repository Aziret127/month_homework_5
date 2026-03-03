from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category, Review


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price'.split()


class ReviewInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewInlineSerializer( many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title description price reviews rating'.split()

    def get_rating(self, obj):
        rating = getattr(obj, 'rating', None)
        if rating is None:
            agg = obj.reviews.aggregate(avg=Avg('stars'))
            rating = agg.get('avg')
        return round(rating, 2) if rating is not None else None


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, obj):
        return obj.product_set.count()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text product stars'.split()

