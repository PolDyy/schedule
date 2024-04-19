from rest_framework import serializers


from apps.schedule import data_types as schedule_types


def validate_day_order(
    previous_day: str,
    prev_day_value: list[schedule_types.TimeSlotType],
    current_day: str,
    curr_day_value: list[schedule_types.TimeSlotType],
):
    """
    Функция валидации, проверяющая порядок открытий и закрытий заведения между днями недели.
    """
    prev_day_last_type = prev_day_value[-1].get('type') if prev_day_value else None
    curr_day_first_type = curr_day_value[0].get('type') if curr_day_value else None

    if prev_day_last_type == 'open' and curr_day_first_type in ['open', None]:
        raise serializers.ValidationError(
            {
                previous_day: [f"The restaurant was opened on {previous_day} and wasn't closed."],
            },
        )
    elif prev_day_last_type in ['close', None] and curr_day_first_type == 'close':
        raise serializers.ValidationError(
            {
                current_day: [
                    f"The restaurant was closed on {current_day} but hadn't been open before that."
                ]
            }
        )


def validate_time_slots(
    day: str,
    time_slots: list[schedule_types.TimeSlotType],
):
    """
    Функция валидации, проверяющая порядок открытий и закрытий заведения на протяжении дня.
    """
    prev_value = None
    prev_type = None

    for slot in time_slots:
        if prev_value is not None:
            if slot['value'] <= prev_value:
                raise serializers.ValidationError(
                    {
                        day: ['The schedule is incorrectly ordered by time'],
                    },
                )
            if slot['value'] - prev_value <= 60:
                raise serializers.ValidationError(
                    {
                        day: ['The time interval between actions should be at least a minute'],
                    },
                )
        prev_value = slot['value']

        if prev_type == 'close' and slot['type'] == 'close':
            raise serializers.ValidationError(
                {
                    day: ['The schedule is incorrectly ordered by actions'],
                },
            )
        elif prev_type == 'open' and slot['type'] == 'open':
            raise serializers.ValidationError(
                {
                    day: ['The schedule is incorrectly ordered by actions'],
                },
            )
        prev_type = slot['type']
