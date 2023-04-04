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
        username = request.data['username']
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
             print(request.data + IntegrityError)
             return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=201)
    

#Auth user
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        try:
            print(User.objects.all())
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(request.data + 'user does not exist')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password, user.password):
            print(request.data + 'credentials wrong')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data)


#Edit password
    def patch(self, request):
        pk = request.data['id']

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            print(request.data + User.DoesNotExist)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.password = make_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


#Delete user
    def delete(self, request):
        pk = request.data['id']
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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