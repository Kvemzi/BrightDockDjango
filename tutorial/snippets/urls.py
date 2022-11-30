
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views


urlpatterns = [
    path('',views.TwitterList.as_view()),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('twitter/', views.TwitterList.as_view()),
    path('twitter/<int:pk>/',views.TwitterDetail.as_view()),
    path('lookup/', views.index_tweet),
    path('lookup/<str:hashtag>/',views.tweets, name="tweets"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
