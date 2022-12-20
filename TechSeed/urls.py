"""TechSeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Admin.views import TermOfUseView, FrequentlyAskedQuestionView, FoundersView
from Blog.views import BlogsView
from Course.views import VideosPlay,  Lessons, \
    CourseListRUD, CourseView, QuestionView, NotesView
from Examination.views import *
from HiringRequest.views import HiringRequestView, EnquiryRequestView, FeedbackView
from Profile.views import myProfile, Signup

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import *

router = DefaultRouter()

router.register('blogs', BlogsView, basename="blog")
router.register('course', CourseView, basename="Course")
router.register('myprofile', myProfile, basename="Create Account")
router.register('signgup', Signup, basename="Create Account")
router.register('course_list', CourseListRUD, basename='Course List')
router.register('lessons', Lessons, basename="Lessons")
router.register('courseStart', VideosPlay, basename='Course Start')
router.register('question', QuestionView, basename='questions')
router.register('hiringrequest', HiringRequestView, basename='Hiring Request')
router.register('enquiryrequest', EnquiryRequestView, basename='Hiring Request')
router.register('feedback', FeedbackView, basename='Feedback')
router.register('notes', NotesView, basename='Notes View')
router.register('termofuse', TermOfUseView, basename='Term Of User')
router.register('faq', FrequentlyAskedQuestionView, basename='Frequently Asked Question')
router.register('founders', FoundersView, basename='Founders')
router.register('examination', SubjectListView, basename='Examination')

admin.AdminSite.site_header = "Jocasta Ai and Robotics Research Center"
admin.AdminSite.site_title = "Welcome to Jocasta"
admin.AdminSite.index_title = "Welcome to Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include("Course.urls")),
    path('gettoken/', token_obtain_pair, name="getToken"),
    path('refreshToken/', token_refresh, name='refreshToken'),
    path('verify', token_verify, name='token_verify'),
    path('summernote/', include('django_summernote.urls')),
    path('payment/', include('Payment.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
