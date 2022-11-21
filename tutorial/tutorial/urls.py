from django.urls import path, include

urlpatterns = [
    path('', include('snippets.urls')),
    path("chat/", include("snippets.urls")),

]
