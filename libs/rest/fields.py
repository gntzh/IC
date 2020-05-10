from rest_framework.serializers import PrimaryKeyRelatedField


class MPrimaryKeyRelatedField(PrimaryKeyRelatedField):

    def __init__(self, to_representation=None, to_internal_value=None, **kwargs):
        if to_representation is not None:
            self.to_representation = to_representation
            self.use_pk_only_optimization = lambda self: False
        if to_internal_value is not None:
            self.to_internal_value = to_internal_value
            self.use_pk_only_optimization = lambda self: False
        super().__init__(**kwargs)
