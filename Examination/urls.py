from django.urls import path
from . import views

# urlpatterns = [
#     path("subject", views.SubjectListView.as_view(),name="subject"),
#     path("subject/create", views.SubjectCreateView.as_view(),name="createSubject"),
#     path("subject/<pk>", views.SubjectUpdateView.as_view(),name="rudSubject"),
#     # -------------------------------------------------------------------------------------
#     path("question", views.QuestionsListView.as_view(),name="subject"),
#     path("question/create", views.QuestionsCreateView.as_view(),name="createQuestion"),
#     path("question/<pk>", views.QuestionsUpdateView.as_view(),name="rudQuestion"),
#     # --------------------------------------------------------------------------------------
#     path("options/<uid>", views.OptionListView.as_view(),name="subject"),
#     path("option/create", views.OptionCreateView.as_view(),name="createOption"),
#     path("option/<pk>", views.OptionUpdateView.as_view(),name="rudOption"),
#     # --------------------------------------------------------------------------------------
# ]