import json

import pytest
from rest_framework.exceptions import ValidationError

from apps.schedule.serializers import WeekScheduleSerializer


@pytest.mark.parametrize(
    'schedule',
    [
        pytest.param(
            {
                'monday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 86399},
                ],
            },
            id='one_open_one_close',
        ),
        pytest.param(
            {
                'monday': [
                    {'type': 'open', 'value': 32400},
                    {'type': 'close', 'value': 39600},
                    {'type': 'open', 'value': 46800},
                    {'type': 'close', 'value': 64800},
                ],
            },
            id='multiple_open_close_times',
        ),
        pytest.param(
            {
                'monday': [{'type': 'open', 'value': 64800}],
                'tuesday': [{'type': 'close', 'value': 14400}],
            },
            id='open_on_one_day_close_on_another',
        ),
    ],
)
def test_validation_correct(schedule):
    """Проверка коректности валидирования с использованием параметризации.

    Валидация с входящими данынми:
    Тест 1: один день с одним открытием и одним закрытием
    Тест 2: один день с двумя открытиями и двумя закрытиями
    Тест 3: открытие в один день закрытие в другой
    """
    serializer = WeekScheduleSerializer(data=schedule)
    assert serializer.is_valid() is True


@pytest.mark.parametrize(
    'schedule, error_message',
    [
        pytest.param(
            {
                'monday': [{'type': 'open', 'value': 0}],
                'tuesday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 86399},
                ],
            },
            '{"monday": ["The restaurant was opened on monday and wasn\'t closed."]}',
            id='never_closed_error',
        ),
        pytest.param(
            {
                'monday': [
                    {'type': 'open', 'value': 32400},
                    {'type': 'open', 'value': 39600},
                    {'type': 'close', 'value': 46800},
                    {'type': 'close', 'value': 64800},
                ],
            },
            '{"monday": ["The schedule is incorrectly ordered by actions"]}',
            id='multiple_open_close_times_error',
        ),
        pytest.param(
            {
                'saturday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 86399},
                ],
                'sunday': [{'type': 'close', 'value': 86399}],
            },
            '{"sunday": ["The restaurant was closed on sunday '
            'but hadn\'t been open before that."]}',
            id='open_on_one_day_close_on_another_error',
        ),
        pytest.param(
            {
                'saturday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 3600},
                    {'type': 'open', 'value': 1800},
                    {'type': 'close', 'value': 5400},
                ],
            },
            '{"saturday": ["The schedule is incorrectly ordered by time"]}',
            id='value_increase_error',
        ),
        pytest.param(
            {
                'saturday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 59},
                ],
            },
            '{"saturday": ["The time interval between actions should be at least a minute"]}',
            id='value_increase_error',
        ),
    ],
)
def test_closed_whole_day_error(schedule, error_message):
    """Проверка коректности валидирования с отрицательным результатом.

    Валидация с входящими данынми:
    Тест 1: было открытие, но не было закрытия
    Тест 2: в один день несколько закртыий и открытий подряд
    Тест 3: закрытие без откртыия
    Тест 4: наружена логика временных интервалов открытия и закрытия
    Тест 5: временной интерпвал между действиями меньше минуты
    """
    serializer = WeekScheduleSerializer(data=schedule)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert json.dumps(exc_info.value.detail) == error_message
