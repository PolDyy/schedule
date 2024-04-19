from typing import TypedDict


class TimeSlotType(TypedDict):
    type: str
    value: int


class WeekScheduleType(TypedDict):
    monday: list[TimeSlotType]
    tuesday: list[TimeSlotType]
    wednesday: list[TimeSlotType]
    thursday: list[TimeSlotType]
    friday: list[TimeSlotType]
    saturday: list[TimeSlotType]
    sunday: list[TimeSlotType]
