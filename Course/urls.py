from django.urls import path
from . import views


urlpatterns = [
    path('livelessons/<Lessons__courses_uid>', views.VideosView.as_view(), name='Videos View')
    # --------------------------------------------------------------------------------------
]