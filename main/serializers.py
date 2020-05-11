from rest_framework import serializers
from libs.rest.fields import MPrimaryKeyRelatedField
from .models import *

__all__ = ('ComponentSerializer', 'RecordSerializer',
           'TypeSerializer', 'AttrSerializer',)


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'


class AttrSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attr
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    types_detail = serializers.SerializerMethodField()
    attrs_detail = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = '__all__'
        extra_kwargs = {
            'types': {'allow_empty': True},
            'attrs': {'allow_empty': True},
        }

    def get_types_detail(self, obj):
        return ({'id': i.id, 'name': i.name} for i in obj.types.all())

    def get_attrs_detail(self, obj):
        return ({'id': i.id, 'name': i.name} for i in obj.attrs.all())


class RecordSerializer(serializers.ModelSerializer):
    component_detail = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = '__all__'

    def get_component_detail(self, obj):
        return ({'id': obj.component.id, 'name': obj.component.name})
