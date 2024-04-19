from rest_framework import serializers

from apps.schedule import validators


class TimeSlotSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['open', 'close'])
    value = serializers.IntegerField(min_value=0, max_value=86399)


class WeekScheduleSerializer(serializers.Serializer):
    monday = TimeSlotSerializer(many=True, default=[])
    tuesday = TimeSlotSerializer(many=True, default=[])
    wednesday = TimeSlotSerializer(many=True, default=[])
    thursday = TimeSlotSerializer(many=True, default=[])
    friday = TimeSlotSerializer(many=True, default=[])
    saturday = TimeSlotSerializer(many=True, default=[])
    sunday = TimeSlotSerializer(many=True, default=[])

    def validate(self, data):
        """
        Функция валидации, проверяющая порядок открытий и закрытий заведения.
        """
        days = list(data.keys())
        for day_index, current_day in enumerate(days):
            previous_day = days[day_index - 1]
            prev_day_value = data[previous_day]
            curr_day_value = data[current_day]
            validators.validate_day_order(
                previous_day=previous_day,
                prev_day_value=prev_day_value,
                current_day=current_day,
                curr_day_value=curr_day_value,
            )
            validators.validate_time_slots(
                day=current_day,
                time_slots=curr_day_value,
            )
        return data
