from django.urls import include, path

urlpatterns = [
    path(
        'api/',
        include(
            ('apps.schedule.urls', 'schedule'),
            namespace='schedule',
        ),
    ),
]
