from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import bookserializer
from .models import book
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET', 'POST'])
def views3(request):
    if request.method == 'GET':
        books = book.objects.all()
        see = bookserializer(books, many=True)
        return Response(see.data)

    if request.method == 'POST':
        ser = bookserializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def view4(request, pk):
    try:
        anyname = book.objects.get(pk=pk)
    except book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serial = bookserializer(anyname)
        return Response(serial.data)

    if request.method == 'PUT':
        serial = bookserializer(anyname, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        anyname.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class apiview1(APIView):

    def get(self, request):
        mname = book.objects.all()
        sname = bookserializer(mname, many=True)
        return Response(sname.data)

    def post(self, request):
        sname = bookserializer(data=request.data)
        if sname.is_valid():
            sname.save()
            return Response(sname.data)
        return Response(sname.errors)


class apiview2(APIView):

    def get_object(self, id):
        try:
            return book.objects.get(id=id)
        except book.doesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        name = self.get_object(id)
        sname = bookserializer(name)
        return Response(sname.data)

    def put(self, request, id):
        name = self.get_object(id)
        sname = bookserializer(name, data=request.data)
        if sname.is_valid():
            sname.save()
            return Response(sname.data)
        return Response(sname.errors)

    def delete(self, request,id):
        name = self.get_object(id)
        name.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class genericview1(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):


    serializer_class = bookserializer
    queryset =  book.objects.all()
    lookup_field = 'id'
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    def post(self, request):
        return self.create(request)
    def put(self, request, id=None):
        return self.update(request, id)
    def delete(self, request, id):
        return self.destroy(request, id )



class apiviewset(viewsets.ModelViewSet):
    serializer_class = bookserializer
    queryset = book.objects.all()

    # def list(self,request):
    #     mname = book.objects.all()
    #     sname = bookserializer(mname, many=True)
    #     return Response(sname.data)
    # def create(self, request):
    #     sname = bookserializer(data=request.data)
    #     if sname.is_valid():
    #         sname.save()
    #         return Response(sname.data)
    #     return Response(sname.errors)
    # def retrieve(self, request, pk=None):
    #      queryset = book.objects.all()
    #      name = get_object_or_404(queryset, pk=pk)
    #      sname = bookserializer(name)
    #      return Response(sname.data)
    # def update(self, request, pk=None):
    #     mname = book.objects.get(pk=pk)
    #     sname = bookserializer(mname, data=request.data)
    #     if sname.is_valid():
    #         sname.save()
    #         return Response(sname.data)
    #     return Response(sname.errors)