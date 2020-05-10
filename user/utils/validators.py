from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


def pwdExist(data):
    try:
        new_password = str(data['new_password'])
        return data
    except KeyError:
        raise ValidationError('new_password为必填字段')


def checkOldPwd(data):
    try:
        new_password = str(data['new_password'])
        old_password = str(data['old_password'])
        username = str(data['username'])
    except KeyError:
        raise ValidationError('字段缺失')

    user = authenticate(username=username, password=old_password)
    if user is not None:
        if old_password != new_password:
            return data
        raise ValidationError('新旧密码相同')
    raise ValidationError('用户不存在')


def CheckUsername(data):
    username = data.get('username', None)
    if username is not None:
        illegal_name = ['admin', 'sure', 'sure.z',
                        'sure.zh', 'django', 'shoor', 'shoorday']
        if username.lower() in illegal_name:
            raise ValidationError('用户名已被使用')
    return data
