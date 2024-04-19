from django.urls import path

from apps.schedule import views as schedule_views

urlpatterns = [
    path(
        'week-schedule/',
        schedule_views.WeekScheduleAPIView.as_view(),
        name='week_schedule',
    ),
]
