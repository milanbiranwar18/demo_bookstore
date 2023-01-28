# Create your views here.

import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializer import RegistrationSerializer, LoginSerializer
from user.utils import JWT

logging.basicConfig(filename="django.log",
                    filemode='a',
                     format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Registration(APIView):
    """
    Class for user Registration
    """

    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode(data={"username": serializer.data.get("username"), "user_id": serializer.data.get("id")})
            return Response({"message":"Registered Successfully", "data":serializer.data, "status":201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class Login(APIView):
    """
    Class for user login
    """

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.data.get("id"))
            token = JWT().encode(data={"user_id": serializer.data.get("id")})
            return Response({"message":"Login Successfully", "status":202, "data":token})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)




class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            decoded = JWT().decode(token)
            user = User.objects.get(username=decoded.get("username"))
            if not user:
                raise Exception("Invalid user")
            user.is_verified = True
            user.save()
            return Response("Token verified")
        except Exception as e:
            logging.exception(e)
            return Response(str(e), status=400)


