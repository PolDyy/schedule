from rest_framework import serializers

from apps.schedule import data_types as schedule_types


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
        Функция валидации, проверяющая порядок открытий и закрытий заведения между днями недели.
        """
        days = list(data.keys())
        for day_index, current_day in enumerate(days):
            previous_day = days[day_index - 1]
            prev_day_value = data[previous_day]
            curr_day_value = data[current_day]
            prev_day_last_type = prev_day_value[-1].get('type') if prev_day_value else None
            curr_day_first_type = curr_day_value[0].get('type') if curr_day_value else None

            if prev_day_last_type == 'open' and curr_day_first_type in ['open', None]:
                raise serializers.ValidationError(
                    {
                        previous_day: [
                            f"The restaurant was opened on {previous_day} and wasn't closed."
                        ],
                    },
                )
            elif prev_day_last_type in ['close', None] and curr_day_first_type == 'close':
                raise serializers.ValidationError(
                    {
                        current_day: [
                            f'The restaurant was closed on {current_day} '
                            f"but hadn't been open before that."
                        ]
                    }
                )
            self.validate_time_slots(
                current_day,
                curr_day_value,
            )
        return data

    def validate_time_slots(
        self,
        day: str,
        time_slots: list[schedule_types.TimeSlotType],
    ):
        """
        Функция валидации, проверяющая порядок открытий и закрытий заведения на протяжении дня.
        """
        prev_value = None
        prev_type = None

        for slot in time_slots:
            if prev_value is not None and slot['value'] <= prev_value:
                raise serializers.ValidationError(
                    {
                        day: ['The schedule is incorrectly ordered by time'],
                    }
                )
            prev_value = slot['value']

            if prev_type == 'close' and slot['type'] == 'close':
                raise serializers.ValidationError(
                    {
                        day: ['The schedule is incorrectly ordered by actions'],
                    }
                )
            elif prev_type == 'open' and slot['type'] == 'open':
                raise serializers.ValidationError(
                    {
                        day: ['The schedule is incorrectly ordered by actions'],
                    }
                )
            prev_type = slot['type']

        return time_slots
