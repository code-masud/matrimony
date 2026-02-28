from django.urls import path
from .views import *

app_name='explore'
urlpatterns = [
    path('', ExploreView.as_view(), name='my_explore')
]
