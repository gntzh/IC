from datetime import timedelta

from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect
import requests
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework.views import Response, status
from rest_framework_simplejwt.tokens import Token, TokenError
from urllib.parse import urlencode

from libs.jwt import get_tokens_for_user
from libs.rest.mixins import ListModelMixin, RetrieveModelMixin
from django.shortcuts import redirect
from .models import OUser
from .utils import serializers, permissions
from .utils.serializers import UserCreateSerializer
from . import tasks

User = get_user_model()


class EmailVerifyToken(Token):
    token_type = 'email_verify'
    lifetime = timedelta(minutes=15)


class VerifyEmailViewSet(ViewSet):

    @action(['post'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def send_verify_url(self, request):
        data = {}
        user = request.user
        if not user.email:
            data['msg'] = '用户未添加邮箱'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        verify_url = '%s/api-user/verify_email?key=%s' % (
            settings.SITE_HOST, EmailVerifyToken.for_user(user))
        tasks.send_verify_email.delay(
            {'username': user.username, 'email': user.email, 'verify_url': verify_url})
        data['msg'] = '已发送邮件'
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=())
    def check_verify_Url(self, request):
        data = {}
        key = request.GET.get('key', None)
        if not key:
            data['msg'] = '无效的链接, 缺失key'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = EmailVerifyToken(key)
        except TokenError:
            data['msg'] = '验证失败'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(id=token['user_id'])
            user.email_is_active = True
            user.save()
            data['msg'] = '验证成功'
            return Response(data)


class UserViewSet(ListModelMixin,
                  mixins.CreateModelMixin,
                  RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    ordering = 'id'

    one_included = many_included = (
        'id', 'username', 'nickname', 'avatar', 'sign')

    @action(detail=False, methods=['post'], permission_classes=())
    def sign_up(self, request):
        request.data['email_is_active'] = False
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        tokens = get_tokens_for_user(user)
        data = serializer.data
        data['tokens'] = tokens
        return Response(data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, included=self.one_included)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(['post', ], detail=True,
            url_path='change_pwd', url_name='change_pwd',
            permission_classes=[permissions.IsOwnerOrAdmin])
    def changePassword(self, request, pk=None):
        return Response(['修改成功'])

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


def check_state(state, expected_type):
    '''state检查
    state约定:identifier_type.redirect.random_value
    '''
    try:
        identifier_type, redirect, random_value = state.split('.')
    except (ValueError, AttributeError):
        return False
    if identifier_type != expected_type:
        return False
    return True


class ThirdPartyLogin(ViewSet):

    @action(detail=False)
    def github(self, request):
        callback = request.query_params.get(
            'callback', reverse('user:auth-github-callback', request=request))
        state = request.query_params.get('state', settings.FRONT_HOST)
        if not check_state(state, 'gh'):
            return Response({'detail': '无效的state'}, status=status.HTTP_404_NOT_FOUND)

        url = 'https://github.com/login/oauth/authorize'+'?' + \
            urlencode({'client_id': '39a0b30fd1c6433d43e1',
                       'redirect_uri': callback,
                       'state': state,
                       })
        return redirect(url)

    @action(detail=False)
    def github_callback(self, request):
        code = request.query_params.get('code')
        if code is None:
            return Response({'detail': '缺失查询参数code'}, status=status.HTTP_404_NOT_FOUND)

        url = 'https://github.com/login/oauth/access_token'
        params = {'code': code,
                  'client_id': settings.GITHUB_APP_KEY,
                  'client_secret': settings.GITHUB_APP_SECRET,
                  }
        res = requests.get(url, params=params, headers={
            'accept': 'application/json'})

        if res.status_code == 200 and not res.json().get('error', False):
            res = requests.get('https://api.github.com/user', headers={
                               'authorization': 'bearer ' + res.json().get('access_token')})
            info = res.json()
            ouser = OUser.objects.filter(
                identifier=info['node_id'], identity_type='gh')
            if ouser.exists():
                u = ouser[0].user
            else:
                u = User.objects.create_user(
                    'gh_' + info['node_id'], avatar=info['avatar_url'])
                OUser(identifier=info['node_id'],
                      identity_type='gh', user=u).save()
            tokens = get_tokens_for_user(u)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({'detail': '无效code'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False)
    def github_userinfo_callback(self, req):
        print(req, req.query_params, dir(req))
        return Response({'token': 'hhhhh'}, status=200)
