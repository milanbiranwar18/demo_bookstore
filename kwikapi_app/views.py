from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from kwikapi import API
from book.models import Book
from book.serialization import BookSerializer



class Books():

    def get(self, request:str) -> str:
        book_list = Book.objects.filter(author=request)
        serializer = BookSerializer(book_list, many=True)
        return serializer.data
   

api = API(default_version='v1')
api.register(Books(), 'v1')
