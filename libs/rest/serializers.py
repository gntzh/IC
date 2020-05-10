from rest_framework import serializers as drf


class ModelSerializer(drf.ModelSerializer):
    """
    A ModelSerializer that takes an additional `excluded` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # 自定义的参数不能传递给ModelSerializer
        excluded = kwargs.pop('excluded', ())
        included = kwargs.pop('included', ())

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        # 白名单优先
        if included:
            included = set(self.fields) - set(included)
            for field_name in included:
                self.fields.pop(field_name, None)
            return

        if excluded:
            # Drop any fields that are not specified in the `fields` argument.
            excluded = set(excluded)
            for field_name in excluded:
                self.fields.pop(field_name, None)
