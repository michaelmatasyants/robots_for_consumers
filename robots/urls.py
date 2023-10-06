from django.urls import path
from .views import create_robot, get_all_robots, get_production_report

urlpatterns = [
    path('add-recently-produced-robot/', create_robot, name='create_robot'),
    path('produced-robots/', get_all_robots, name='get_robots'),
    path('report/', get_production_report, name='production_report'),
]
