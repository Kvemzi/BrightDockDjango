
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
    path('twitter/', views.twitter_list),
    path('twitter/<int:pk>/',views.twitter_details),
    path('notification/',views.testiranj)
    path('twitter/latest',views.twitter_latest),

]

urlpatterns = format_suffix_patterns(urlpatterns)
