from django.http.response import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .Serializers import *
from .models import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CourseListRUD(ModelViewSet):
    queryset = CourseList.objects.all()
    serializer_class = CourseListSerial
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get']


class CourseView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerial
    lookup_field = "uid"
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course_title',"uid"]
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get']


class Lessons(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerial
    lookup_field = "courses__uid"

    def get_queryset(self):
        if 'courses' in self.kwargs:
            return Lesson.objects.filter(courses__uid=self.kwargs['courses'])
        else:
            raise ValidationError("No Course ")


class VideosView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerial
    SearchFilter = ["$Lessons", "uid"]
    pagination_class = StandardResultsSetPagination
    lookup_url_kwarg = "Lessons__courses_uid"
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        video = Video.objects.filter(Lessons__courses__uid=uid).values('Lessons__Lesson_Name', 'title', "time", "uid").order_by("Lessons__updatedAt")
        data = self.merge(video)
        return JsonResponse(data, content_type='application/json', safe=False)

    @staticmethod
    def merge(dicts):
        res = []

        for key in set(dict['Lessons__Lesson_Name'] for dict in dicts):
            res.append({'Lesson': key, 'video': []})

        for d in dicts:
            for r in res:
                data = dict()
                if d['Lessons__Lesson_Name'] == r['Lesson']:
                    data['title'] = d['title']
                    data['uid'] = d['uid']
                    data['time'] = d['time']
                    r['video'].append(data)
        return res


class VideosPlay(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerial
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "Lessons"

    def get_queryset(self):
        if 'Lessons' in self.kwargs:
            value = Video.objects.filter(Lessons__courses=self.kwargs['Lessons'])
            return value
        else:
            raise ValidationError("No Lessons declare ")

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)


class QuestionView(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerial
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class NotesView(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerial
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        return Note.objects.filter(by__email=self.request.user.email, video=self.kwargs['uid'])

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data, status=HTTP_302_FOUND)
