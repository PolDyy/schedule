import datetime
import copy

from apps.schedule import data_types as schedule_types


class ScheduleService:
    """Класс работы с рассписанием."""

    def __init__(
        self,
        schedule: schedule_types.WeekScheduleType,
    ):
        self.schedule = self._rebuild(schedule)

    def get_schedule(self) -> str:
        """Возвращает удобочитаемую версию расписания работы."""
        schedule = self.schedule
        result = []
        for week_day, timeslot in schedule.items():
            week_day = week_day.capitalize()
            if not timeslot:
                time_str = 'Closed'
            else:
                time_str = self._get_schedule_time_str(timeslot)
            result.append(f'{week_day}: {time_str}')
        return '\n'.join(result)

    def _get_schedule_time_str(
        self,
        schedule_time: list[schedule_types.TimeSlotType],
    ) -> str:
        """
        Преобразует список действий за день в строку,
        представляющую временные интервалы.
        """
        result = []
        time_pairs = zip(schedule_time[::2], schedule_time[1::2])
        for open_slot, close_slot in time_pairs:
            if open_slot['type'] == 'open' and close_slot['type'] == 'close':
                open_time = self._convert_time(open_slot['value'])
                close_time = self._convert_time(close_slot['value'])
                result.append(f'{open_time} - {close_time}')
            else:
                raise ValueError('Actions conflict in schedule')
        return ', '.join(result)

    @staticmethod
    def _rebuild(
        schedule: schedule_types.WeekScheduleType,
    ) -> schedule_types.WeekScheduleType:
        """
        Перемещает время закрытия со следующего дня недели,
        если в текущий день заведение не было закрыто.
        """
        schedule = copy.deepcopy(schedule)
        days = list(schedule.values())
        for day_index, current_day in enumerate(days):
            previous_day = days[day_index - 1]
            prev_day_last_type = previous_day[-1].get('type') if previous_day else None
            if prev_day_last_type in ['close', None]:
                continue
            curr_day_first_timeslot = current_day.pop(0) if current_day else None
            previous_day.append(curr_day_first_timeslot)
        return schedule

    @staticmethod
    def _convert_time(seconds: int) -> str:
        """Преобразует секунды в строку формата 12-часового времени."""
        time = datetime.timedelta(seconds=seconds)
        time_str = (datetime.datetime.min + time).strftime('%I:%M %p').lstrip('0')
        return time_str
