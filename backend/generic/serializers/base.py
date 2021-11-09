"""
Class implementations of generic views or viewsets meant to be used through
out EJJY for DRYness and maintainability.
"""
from rest_framework import serializers

### File Specific Pylint Configuration ###
# unnecessary - pylint: disable=abstract-method


def _extract_fields(fields, allowed_fields):
    """Extract Fields

    Removes fields in `fields` based on `allowed_fields`. `fields` will be
    mutated instead of returned, so this must be a reference to the actual
    `fields` attribute of a serializer.

    Args:
        fields (dict of str: Serializer): A dictionary of fields from the
            serializer.
        allowed_fields (set of str): A set a of allowed fields. If
            `allowed_fields` is empty or `None`, `fields` will remain
            unchanged.
    """
    if allowed_fields:

        existing_fields = set(fields.keys())
        for field in existing_fields - allowed_fields:
            fields.pop(field)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """Dynamic Fields Model Serializer

    A Generic Model Serializer that supports dynamic fields. Identical to
    `DynamicFieldsSerializer` except that it inherits from
    `ModelSerializer` and not `Serializer`.
    """

    class Meta:
        abstract = True

    @property
    def fields(self):
        """Fields

        Overrides parent property `fields()` to filter fields dynamically.

        Convention for field filtering is as follows:

        `fields` is reserved for top level field filtering and not for
        nested fields.

        '<field_name>__fields` is used for nested fields.

        `<parent_field_name>__` maybe be appended to the beginning of the
        initial string for as many parents the nested field has.
        """
        all_fields = super().fields

        field_name = self.field_name

        if not field_name:
            context_key = "fields"
        else:
            field_names = list()
            parent = self.parent

            while field_name:
                field_names.append(field_name)
                field_name = parent.field_name
                parent = parent.parent

            if field_names and len(field_names) > 1:
                field_names.reverse()

            field_names.append("fields")

            context_key = "__".join(field_names)

        fields = self.context.get(context_key, None)

        if fields:
            _extract_fields(all_fields, set(fields))

        return all_fields


class DynamicFieldsSerializer(serializers.Serializer):
    """Dynamic Fields Serializer

    A Generic Serializer that supports dynamic fields. Identical to
    `DynamicModelFieldsSerializer` except that it inherits from
    `Serializer` and not `ModelSerializer`.
    """

    class Meta:
        abstract = True

    @property
    def fields(self):
        """Fields

        Overrides parent property `fields()` to filter fields dynamically.

        Convention for field filtering is as follows:

        `fields` is reserved for top level field filtering and not for
        nested fields.

        '<field_name>__fields` is used for nested fields.

        `<parent_field_name>__` maybe be appended to the beginning of the
        initial string for as many parents the nested field has.
        """
        all_fields = super().fields

        field_name = self.field_name

        if not field_name:
            context_key = "fields"
        else:
            field_names = list()
            parent = self.parent

            while field_name:
                field_names.append(field_name)
                field_name = parent.field_name
                parent = parent.parent

            if field_names and len(field_names) > 1:
                field_names.reverse()

            field_names.append("fields")

            context_key = "__".join(field_names)

        fields = self.context.get(context_key, None)

        if fields:
            _extract_fields(all_fields, set(fields))

        return all_fields
