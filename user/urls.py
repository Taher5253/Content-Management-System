from django.urls import path
from .views import *
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('content/', ContentAPI.as_view(), name='content'),
    path('categories/', CategoriesAPI.as_view(), name='categories'),
    path('content/<int:pk>/', ContentAPI.as_view(), name='deletecontent'),
    path('getcontentcategories/', GetCategoriesAPI.as_view(), name='getcontentcategories'),
    path('categories/<int:pk>/', CategoriesAPI.as_view(), name='updatecategories'),
    path('search/', views.SearchAPIView.as_view(), name='search'),
    path('searchcategory/', views.SearchByCategory.as_view(), name='searchcategory')
    ]