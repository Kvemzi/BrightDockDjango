
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views


urlpatterns = [
    path('', views.index),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('twitter/', views.TwitterList.as_view()),
    path('twitter/<int:pk>/', views.TwitterDetail.as_view()),
    path('simple_function', views.simple_function)
]

urlpatterns = format_suffix_patterns(urlpatterns)