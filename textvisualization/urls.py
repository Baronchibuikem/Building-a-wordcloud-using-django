from django.urls import path
from textvisualization import views


urlpatterns = [
    path("", views.WordCloudView.as_view(), name="wordcloud"),
]
