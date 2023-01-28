from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from cart.serializer import  CartSerializer

import logging

from user.utils import verify_token, verify_superuser

logging.basicConfig(filename="cart.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class CartAPI(APIView):

    @verify_token
    def post(self, request):
        """
        Function for adding books to the cart
        """
        try:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Cart Created Successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': str(e), 'status': 400}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        Function for get carts
        """
        try:
            item_list = Cart.objects.filter(user= request.data.get('user'))
            serializer = CartSerializer(item_list, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


    @verify_token
    def delete(self, request, pk):
        """
        Function for delete cart
        """
        try:
            id = pk
            cart = Cart.objects.get(pk=id)
            print(cart)
            cart.delete()
            return Response({"Message": "Cart Deleted Successfully", "status": 204})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


class CheckoutAPI(APIView):
    @verify_token
    def put(self, request):
        user = Cart.objects.get(user=request.data.get("user"), status=False)
        print(user)
        if user is not None:
            user.status = True
            user.save()
            print(user.save())
        return Response({"Message": "status updated Successfully", 'status':200})