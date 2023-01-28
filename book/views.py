import logging

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serialization import BookSerializer
from user.utils import verify_token, verify_superuser

logging.basicConfig(filename="book.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Books(APIView):
    """
    Class for performing curd operation for book
    """
    @verify_token
    def post(self, request):
        """
        Function for add book
        """
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Book Added Successfully', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)


    def get(self, request):
        """
        Function for get book
        """
        try:
            book_list = Book.objects.all()
            serializer = BookSerializer(book_list, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_superuser
    def put(self, request, pk):
        """
        Function for update book information
        """
        try:
            id = pk
            book = Book.objects.get(pk=id)
            serialiser = BookSerializer(book, data=request.data, partial=True)
            if serialiser.is_valid():
                serialiser.save()
                return Response({"Messsage": "Book Updated Successfully", "status": 201})
            return Response(serialiser.errors, status=400)
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_superuser
    def delete(self, request, pk):
        """
        Function for delete book
        """
        try:
            id = pk
            book = Book.objects.get(pk=id)
            book.delete()
            return Response({"Message": "Book Deleted Successfully", "status": 204})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
