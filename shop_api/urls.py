"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from django.contrib import admin
from django.urls import path, include

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('reviews', ReviewViewSet)

#urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include(router.urls)),
    path('api/v1/product/<int:pk>/',include(router.urls)),
    path('api/v1/categories/', include(router.urls)),
    path('api/v1/category/<int:pk>/', include(router.urls)),
    path('api/v1/reviews/', include(router.urls)),
    path('api/v1/review/<int:pk>/', include(router.urls)),
    path('api/v1/users/', include('users.urls')),
]




# from django.urls import path, include
# from django.contrib import admin
# from rest_framework.routers import DefaultRouter
# from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet

# router = DefaultRouter()
# router.register('products', ProductViewSet,)
# router.register('categories', CategoryViewSet,)
# router.register('reviews', ReviewViewSet,)
# # router.register(r'reviews', views.ReviewViewSet, basename='review')



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/', include('product.urls')),
#    # path('api/v1/products/', views.product_list_api_view),
#     path('api/v1/products/', include(router.urls)),
#     # path('api/v1/products/reviews/', views.product_reviews_list_api_view),
#    # path('api/v1/product/<int:pk>/', views.product_detail_api_view),
#     path('api/v1/categories/', include(router.urls)),
#     path('api/v2/categories/', views.category_list_api_view) ,
#     path('api/v2/category/<int:pk>/', views.category_detail_api_view),
#     path('api/v1/reviews/', include(router.urls)),
#     # path('api/v1/reviews/', views.review_list_api_view),
#     # path('api/v1/review/<int:pk>/', views.review_detail_api_view),
#     ]

