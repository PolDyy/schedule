import pytest

from apps.schedule.services import ScheduleService


@pytest.mark.parametrize(
    'schedule, expected_result',
    [
        pytest.param(
            {
                'monday': [
                    {'type': 'open', 'value': 0},
                    {'type': 'close', 'value': 3600},
                ],
                'tuesday': [],
            },
            'Monday: 12:00 AM - 1:00 AM\nTuesday: Closed',
            id='one_open_on_close',
        ),
        pytest.param(
            {
                'monday': [
                    {'type': 'open', 'value': 36000},
                    {'type': 'close', 'value': 55800},
                    {'type': 'open', 'value': 57600},
                    {'type': 'close', 'value': 72000},
                ],
            },
            'Monday: 10:00 AM - 3:30 PM, 4:00 PM - 8:00 PM',
            id='multiple_open_close_times',
        ),
        pytest.param(
            {
                'saturday': [
                    {'type': 'open', 'value': 72000},
                ],
                'sunday': [
                    {'type': 'close', 'value': 3600},
                ],
            },
            'Saturday: 8:00 PM - 1:00 AM\nSunday: Closed',
            id='open_on_one_day_close_on_another',
        ),
    ],
)
def test_get_schedule(schedule, expected_result):
    """Проверка коректности выдачи рассписания.

    Описание данных параметризации:
    Тест 1: один день с одним открытием и одним закрытием
    Тест 2: один день с двумя открытиями и двумя закрытиями
    Тест 3: открытие в один день закрытие в другой
    """
    service = ScheduleService(schedule)
    assert service.get_schedule() == expected_result


def test_get_schedule_error():
    """Проверка коректности выдачи рассписания с отрицательым результатом."""
    schedule = {
        'monday': [
            {'type': 'open', 'value': 36000},
            {'type': 'open', 'value': 55800},
        ],
    }
    error_message = 'Actions conflict in schedule'
    service = ScheduleService(schedule)
    with pytest.raises(ValueError) as exc_info:
        service.get_schedule()
    assert str(exc_info.value) == error_message
