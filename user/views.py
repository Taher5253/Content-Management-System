from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from user.serializers import *
from django.contrib.auth import authenticate
from rest_framework import filters
from rest_framework import generics

from django.views import View
from rest_framework.parsers import MultiPartParser, FormParser
import re
# Create your views here.






class Register(APIView):
    """
    Register API
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data['email']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            password = request.data['password']
            confirm_password = request.data['confirm_password']
            phone_number = request.data['phone_number']
            address = request.data['address']
            city = request.data['city']
            state = request.data['state']
            country = request.data['country']
            pincode = request.data['pin-code']
        except:
            return Response({'result': 'Missing or incorrect fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(request.data)
            if not first_name.strip() or not last_name.strip():
                return Response({'result': 'Firstname and Lastname must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if password == confirm_password:
                    pattern = "^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9\S]{8,}$"
                    result = re.findall(pattern, password)
                    if result:
                        user = User.objects.create_user(username=email, email=email, first_name=first_name,
                                        last_name=last_name, password=str(password), is_active=True)
                        if user:
                            cms_user = Cms_user.objects.create(user_id=user.id, address = address, city = city, state = state, phone_number = phone_number, country = country, pincode= pincode)
                            if cms_user:
                                return Response({'result': 'user created'}, status=status.HTTP_201_CREATED)
                            else:
                                return Response({'result': 'cms user not created'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'result': 'user not created'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'result': 'Your password must contain at least eight characters consisting of one uppercase letter and one lowercase letter'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'result': 'password and confirm does not match'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    """

    Login  API

    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            email = request.data.get("email-id")
            password = request.data.get("password")

            if not email.strip() or not password.strip():
                return Response({'result': 'Enter email-id and password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_data = User.objects.filter(email=email).first()
                if user_data:
                    user = authenticate(username=user_data.username, password=password)
                    if not user:
                        return Response({"error": "email-id or password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response({"token": token.key}, status=status.HTTP_200_OK)

                else:
                    return Response({"error": "Login failed user does not exists"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)


class ContentAPI(APIView):
    """

    Content API for creating content, updating content, reading content, deleting content

    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            usr = request.user.id
            cms_user = Cms_user.objects.filter(user_id=usr).first()
            data = request.data
            data['content_author'] = cms_user.id
            content_serializer = ContentSerializer(data=data)
            if content_serializer.is_valid():
                content_serializer.save()
                return Response(content_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        try:
            usr = request.user.id
            user_data = User.objects.filter(id=usr).first()
            if user_data.is_staff:
                content_data = Content.objects.all()
                if content_data:
                    serializer = ContentReadSerializer(content_data, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No content'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                cms_user = Cms_user.objects.filter(user_id=usr).first()
                content_data = Content.objects.filter(content_author_id=cms_user.id)
                if content_data:
                    serializer = ContentReadSerializer(content_data, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            usr = request.user.id
            user_data = User.objects.filter(id=usr).first()
            if user_data.is_staff:
                content_data = Content.objects.filter(id=pk).first()
                if content_data:
                    content_data.delete()
                    category_data = content_category.objects.filter(content_id=pk)
                    category_data.delete()
                    return Response({'result': 'Deleted Successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No content'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                cms_user = Cms_user.objects.filter(user_id=usr).first()
                content_data = Content.objects.filter(content_author_id=cms_user.id, id=pk).first()
                if content_data:
                    content_data.delete()
                    category_data = content_category.objects.filter(content_id=pk)
                    category_data.delete()
                    return Response({'result': 'Deleted Successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            content = Content.objects.filter(id=pk).first()
            if content:
                usr = request.user.id
                user_data = User.objects.filter(id=usr).first()
                if user_data.is_staff:
                    content.title = request.data.get('title')
                    content.body = request.data.get('body')
                    content.summary = request.data.get('summary')
                    content.document_pdf = request.data.get('document_pdf')
                    content.content_author_id = cms_user.id
                    content.save()
                    return Response({'result': "Updated Successfully"}, status=status.HTTP_200_OK)
                else:
                    cms_user = Cms_user.objects.filter(user_id=usr).first()
                    content.title = request.data.get('title')
                    content.body = request.data.get('body')
                    content.summary = request.data.get('summary')
                    content.document_pdf = request.data.get('document_pdf')
                    content.content_author_id = cms_user.id
                    content.save()
                    return Response({'result': "Updated Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({'result': 'No content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

class CategoriesAPI(APIView):
    """

    Categories API for content
    create categories, update and delete categories for content

    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        try:
            usr = request.user.id
            cms_user = Cms_user.objects.filter(user_id=usr).first()
            content_id = request.data.get('content')
            content_author_data = Content.objects.filter(id=content_id).first()
            if content_author_data:
                if cms_user.id == content_author_data.content_author_id:
                    categories = request.data.get('category')
                    for i in range(len(categories)):
                        category_exists = content_category.objects.filter(content_id=content_id, category_id=categories[i]).exists()
                        if category_exists:
                            pass
                        else:
                            content_category.objects.create(content_id=content_id, category_id=categories[i])

                    return Response({'result': 'Categories added successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'result': 'Content does belong to author'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            usr = request.user.id
            content_author_data = Content.objects.filter(id=pk).first()
            if content_author_data:
                user_data = User.objects.filter(id=usr).first()
                if user_data.is_staff:
                    category_update = request.data.get('category')
                    for i in range(len(category_update)):
                        category_exists = content_category.objects.filter(content_id=pk, category_id=category_update[i]).exists()
                        if category_exists:
                            pass
                        else:
                            content_category.objects.create(content_id=pk, category_id=category_update[i])
                    return Response({'result': "Updated Successfully"}, status=status.HTTP_201_CREATED)
                else:
                    cms_user = Cms_user.objects.filter(user_id=usr).first()
                    if content_author_data.content_author_id == cms_user.id:
                        category_update = request.data.get('category')
                        for i in range(len(category_update)):
                            category_exists = content_category.objects.filter(content_id=pk, category_id=category_update[i]).exists()
                            if category_exists:
                                pass
                            else:
                                content_category.objects.create(content_id=pk, category_id=category_update[i])
                        return Response({'result': "Updated Successfully"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'result': "Content does belong to author"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            usr = request.user.id
            content_author_data = Content.objects.filter(id=pk).first()
            if content_author_data:
                user_data = User.objects.filter(id=usr).first()
                if user_data.is_staff:
                    category_delete = request.data.get('category')
                    for i in range(len(category_delete)):
                        category_exists = content_category.objects.filter(content_id=pk, category_id=category_delete[i]).exists()
                        if category_exists:
                            content_category_del = content_category.objects.filter(content_id=pk, category_id=category_delete[i]).first()
                            content_category_del.delete()
                        else:
                            pass
                    return Response({'result': "Deleted Successfully"}, status=status.HTTP_200_OK)
                else:
                    cms_user = Cms_user.objects.filter(user_id=usr).first()
                    if content_author_data.content_author_id == cms_user.id:
                        category_delete = request.data.get('category')
                        for i in range(len(category_delete)):
                            category_exists = content_category.objects.filter(content_id=pk, category_id=category_delete[i]).exists()
                            if category_exists:
                                content_category_del = content_category.objects.filter(content_id=pk, category_id=category_delete[i]).first()
                                content_category_del.delete()
                            else:
                                pass
                        return Response({'result': "Deleted Successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'result': "Content does belong to author"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)



class GetCategoriesAPI(APIView):
    """

    API for fetching content and categories in detail

    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request, format=None):
        try:
            usr = request.user.id
            user_data = User.objects.filter(id=usr).first()
            content_id = request.data.get('content-id')
            if user_data.is_staff:
                content_data = content_category.objects.filter(content_id=content_id)
                if content_data:
                    serializer = content_categorySerializer(content_data, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                cms_user = Cms_user.objects.filter(user_id=usr).first()
                content_data_cms = Content.objects.filter(id=content_id).first()
                if content_data_cms.content_author_id == cms_user.id:
                    content_data = content_category.objects.filter(content_id=content_id)
                    if content_data:
                        serializer = content_categorySerializer(content_data, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)

class SearchAPIView(generics.ListCreateAPIView):
    """

    Search API for content by title, body and summary

    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    search_fields = ['title', 'body', 'summary']
    filter_backends = (filters.SearchFilter,)
    queryset = Content.objects.all()
    serializer_class = ContentReadSerializer


class SearchByCategory(APIView):
    """

    Search API by category

    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        try:
            search = request.data.get('search')
            category_search = Categories.objects.filter(category_type__contains=search.lower())
            if category_search:
                data = content_category.objects.filter(category_id=category_search[0].id)
                if data:
                    serializer = content_categorySerializer(data, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'No Content'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'result': 'Something went wrong please try again later'}, status=status.HTTP_400_BAD_REQUEST)