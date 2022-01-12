from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from .models import book
from .serializer import bookserializer
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
def fun1(request):

    if request.method == 'GET':
        mname = book.objects.all()
        sname = bookserializer(mname, many=True)
        return Response(sname.data)

    if request.method == 'POST':
        sname = bookserializer(book, data=request.data)
        if sname.is_valid():
            sname.save()
            return Response(sname.data)
        return Response(sname.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def fun2(request, pk):

    try:
        mname = book.objects.get(pk=pk)
    except book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        sname = bookserializer(mname)
        return Response(sname.data)

    if request.method == 'PUT':
        sname = bookserializer(mname, data=request.data)
        if sname.is_valid():
            sname.save()
            return Response(sname.data)
        return Response(sname.errors)

    if request.method == 'DELETE':
        mname.delete()
        return Response(status=204)

class v1(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = bookserializer
    queryset = book.objects.all()