from datetime import date as d
from rest_framework import serializers


def not_earlier_today_validator(date):
    if date < d.today():
        raise serializers.ValidationError("It is forbidden to set past dates!")
    return date
