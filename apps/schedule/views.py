from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.schedule import serializers as schedule_serializers
from apps.schedule import data_types as schedule_types
from apps.schedule import services as schedule_services


class WeekScheduleAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = schedule_serializers.WeekScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule_data: schedule_types.WeekScheduleType = serializer.validated_data
            try:
                schedule = schedule_services.ScheduleService(schedule_data).get_schedule()
            except ValueError as e:
                return Response({'non_field_errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'schedule': schedule}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
