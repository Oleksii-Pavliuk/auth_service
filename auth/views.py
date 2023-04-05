from django.db.utils import IntegrityError
from django.http import Http404, HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from django.http import HttpResponseServerError
from requests.exceptions import ConnectionError
from rest_framework.permissions import IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey


from .models import User
from .serializers import UserSerializer


# Create your views here.


class UserAuth(APIView):
    permission_classes = [HasAPIKey | IsAdminUser]
# Add user
    def put(self, request):
        try:
            username = request.data['username']
            email = request.data["email"]
            password = request.data["password"]
            user = User.objects.create_user(username, email, password)
            serializer = UserSerializer(user)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=201)
        except (IntegrityError, KeyError, User.DoesNotExist):
            print('bad request\n')
            print(request.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)

#Auth user
    def post(self, request):
        print(request.data)
        try:
            username = request.data["username"]
            password = request.data["password"]

            print(User.objects.all())
            user = User.objects.get(username=username)

            if not check_password(password, user.password):
                print('credentials wrong \n')
                print(request.data)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            else:
                serializer = UserSerializer(user)
                return Response(serializer.data)
        except (IntegrityError, KeyError, User.DoesNotExist):
            print('bad request\n')
            print(request.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)


#Edit password
    def patch(self, request):
        try:
            pk = request.data['id']
            user = User.objects.get(pk=pk)
            user.password = make_password(request.data['password'])
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except (IntegrityError, KeyError, User.DoesNotExist):
            print('bad request\n')
            print(request.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)


#Delete user
    def delete(self, request):
        try:
            pk = request.data['id']
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (IntegrityError, KeyError, User.DoesNotExist):
            print('bad request\n')
            print(request.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)

#Consul health check
def health_check(request):
    try:
        # add health check code here
        return HttpResponse("Healthy")
    except ConnectionError as e:
        # print the error message to console or log file
        print(f"Error: {str(e)}")
        return HttpResponseServerError("Connection Error")
    except Exception as e:
        # print the error message to console or log file
        print(f"Error: {str(e)}")
        return HttpResponseServerError("Internal Server Error")