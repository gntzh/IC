import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from libs.rest.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'email_is_active',
                  'last_login', 'avatar', 'sign', 'phone', 'is_staff']
        extra_kwargs = {
            'username': {'required': True, },
            'password': {'write_only': True, 'required': True, 'help_text': '必填'},
            'email': {'label': '邮箱'},
            'email_is_active': {'read_only': True},
            'last_login': {'read_only': True, 'format': '%Y-%m-%d %H:%M:%S'},
            'avatar': {'help_text': '一个URL'}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'email_is_active', 'phone']
        extra_kwargs = {
            'username': {'required': True, 'validators': (RegexValidator(r'^(admin|shoor|sure)', '用户名不能以sure/admin/shoor开头', inverse_match=True, flags=re.I), )},
            'password': {'write_only': True, 'required': True, 'help_text': '必填'},
            'email': {'label': '邮箱', 'validators': [RegexValidator(
                r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-zd]+[-.])+[A-Za-zd]{2,5}$', '无效邮箱')]},
            'email_is_active': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email',
                  'avatar', 'phone', 'old_password']
        extra_kwargs = {
            'password': {'required': False},
            'email': {'label': '邮箱', 'required': False},
            'username': {'required': True},
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            user = super().update(instance, validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        return super().update(instance, validated_data)


class UserInfoSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', ]


class UserField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def __init__(self, method=None, **kwargs):
        self.method = method
        kwargs.setdefault('queryset', User.objects.all())
        kwargs.setdefault('default', serializers.CurrentUserDefault())
        super().__init__(**kwargs)

    def to_internal_value(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=pk)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(pk).__name__)

    def to_representation(self, user):
        if self.method is not None:
            return self.method(user)
        return UserInfoSerializer(user).data
