"""
"""
from rest_framework import serializers


class CommaSeparatedIntegersField(serializers.Field):
    """Comma Separated Integers

    Gets a string comma separated integers and deserializes it into a list of
    `int`.

    If any of the comma separated values is a non-digit, a `ValidationError`
    will be raised.
    """

    # accessible to child classes in case they want to keep things consistent
    help_text = "Comma separated integers. E.g. `1,2,3,4,5`, `19`, `-1,3`."

    def __init__(self, **kwargs):
        if "help_text" not in kwargs:
            kwargs["help_text"] = CommaSeparatedIntegersField.help_text
        super().__init__(**kwargs)

    def to_representation(self, value):

        return "".join(map(str, value))

    def to_internal_value(self, data):

        data_list = data.split(",")

        for value in data_list:
            if not value.isdigit():
                raise serializers.ValidationError("Invalid integer value `%s`." % value)

        return [int(value) for value in data_list]


class CommaSeparatedStringsField(serializers.Field):
    """Comma Separated Strings

    Gets a string comma separated strings and deserializes it into a list of
    `str`.
    """

    # accessible to child classes in case they want to keep things consistent
    help_text = "Comma separated strings. E.g. `a,b,c`, `eAsY,HaRd`, `X,Y,Z`."

    def __init__(self, **kwargs):
        if "help_text" not in kwargs:
            kwargs["help_text"] = CommaSeparatedIntegersField.help_text
        super().__init__(**kwargs)

    def to_representation(self, value):

        return "".join(map(str, value))

    def to_internal_value(self, data):

        return data.split(",")
