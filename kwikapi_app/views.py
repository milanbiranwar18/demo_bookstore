from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from kwikapi import API
from book.models import Book
from book.serialization import BookSerializer
import json


class Books():

    def get(self, title:str, author:str) -> list:
        book_list = Book.objects.filter(title=title, author=author)
        serializer = BookSerializer(book_list, many=True)
        print(type(serializer.data))
        return serializer.data
   

api = API(default_version='v1')
api.register(Books(), 'v1')
