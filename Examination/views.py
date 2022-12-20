from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from .Serializers import *


class SubjectListView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = Subjects
    lookup_url_kwarg = "uid"


class QuestionsListView(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerial
    authentication_classes = [JWTAuthentication]
    permission = [IsAuthenticatedOrReadOnly]


class OptionListView(ModelViewSet):
    serializer_class = Options
    authentication_classes = [JWTAuthentication]
    permission = [IsAuthenticated]
    http_method_names = ['get']
    lookup_url_kwarg = 'uid'

    def list(self, request, *args, **kwargs):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        option = Option.objects.filter(Question__subjects=uid)
        data = self.merge(option.values('Question__questions', 'option', 'imagesOptions', 'is_correct_answer'))
        return JsonResponse(data, content_type='application/json', safe=False)

    @staticmethod
    def merge(dicts):
        res = []

        for key in set(dict['Question__questions'] for dict in dicts):
            res.append({'Question': key, 'option': [],
                        'imagesOptions': [], 'is_correct_answer': []})

        for d in dicts:
            for r in res:
                if d['Question__questions'] == r['Question']:
                    r['option'].append(d['option'])
                    r['imagesOptions'].append(d['imagesOptions'])
                    r['is_correct_answer'].append(d['is_correct_answer'])
        return res


# class OptionCreateView(CreateAPIView):
#     queryset = Option
#     serializer_class = Options
#     authentication_classes = [JWTAuthentication]
#     permission = [IsAuthenticatedOrReadOnly]
#
#
# class OptionUpdateView(RetrieveUpdateDestroyAPIView):
#     queryset = Option
#     serializer_class = Options
#     authentication_classes = [JWTAuthentication]
#     permission = [IsAuthenticatedOrReadOnly]
