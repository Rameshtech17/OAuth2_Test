from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests
from .serializers import CreateUserSerializer, SchoolSerializer, ClassSerializer, TeacherSerializer, StudentListSerializer, SubjectSerializer, TeachersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import School, Class, Teacher, Student, Subject
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import status, generics






CLIENT_ID = 'Uy1BAWOmJ3r3hJI6jHqzw5R7zOocjI5u3qe1FeJU'
CLIENT_SECRET = 'CrFJk3XnyySMIA0GZeFHVJqvTYJJLDXUd7UWtvwtn5WUgrLUsU6fGt6mHhYBIwUuygxehY6TBYDlpUCnagjTiRnGPWpgXMdt2cWjNFH6nMBwIXzbLSvdLggGcDe05OY6'



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        r = requests.post('http://127.0.0.1:8000/o/token/',
                          data={
                              'grant_type': 'password',
                              'username': request.data['username'],
                              'password': request.data['password'],
                              'client_id': CLIENT_ID,
                              'client_secret': CLIENT_SECRET,
                          },
                          )
        return Response(r.json())
    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://127.0.0.1:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)




class SchoolAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        school = School.objects.all()
        serializer = SchoolSerializer(school, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassSearchAPIView(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    # filter_fields = ('ClassName', )
    search_fields = ('ClassName',)


class SearchAPIView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('Class', 'TeacherName')
    # search_fields = ('id'.'Class', 'TeacherName')


class ClassAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        Clas = Class.objects.all()
        serializer = ClassSerializer(Clas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        teacher = Teacher.objects.all()
        serializer = TeachersSerializer(teacher, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeachersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        student = Student.objects.all()
        serializer = StudentListSerializer(student, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        subject = Subject.objects.all()
        serializer = SubjectSerializer(subject, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolUpdateAPIView(APIView):

    def get_object(self, id):
        try:
            return School.objects.get(id=id)

        except School.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        school = self.get_object(id)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)

    def put(self, request, id):
        school = self.get_object(id)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        school = self.get_object(id)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClassUpdateAPIView(APIView):

    def get_object(self, id):
        try:
            return Class.objects.get(id=id)

        except Class.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        Clas = self.get_object(id)
        serializer = ClassSerializer(Clas)
        return Response(serializer.data)

    def put(self, request, id):
        Clas = self.get_object(id)
        serializer = ClassSerializer(Clas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Class = self.get_object(id)
        Class.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherUpdateAPIView(APIView):

    def get_object(self, id):
        try:
            return Teacher.objects.get(id=id)

        except Teacher.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        teacher = self.get_object(id)
        serializer = TeachersSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, id):
        teacher = self.get_object(id)
        serializer = TeachersSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        teacher = self.get_object(id)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentListUpdateAPIView(APIView):

    def get_object(self, id):
        try:
            return Student.objects.get(id=id)

        except Student.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = StudentListSerializer(student)
        return Response(serializer.data)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = StudentListSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubjectUpdateAPIView(APIView):

    def get_object(self, id):
        try:
            return Subject.objects.get(id=id)

        except Subject.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        teacher = self.get_object(id)
        serializer = SubjectSerializer(teacher)
        return Response(serializer.data)

    def put(self, request, id):
        teacher = self.get_object(id)
        serializer = SubjectSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        teacher = self.get_object(id)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class ShowProfile(APIView):
#
#     permission_classes = [IsAuthenticated, IsAdminUser]
#
#     def get(self, request):
#         serializer = showProfileSerializer(request.user)
#         return Response(serializer.data)
