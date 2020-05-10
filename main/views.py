from django.db import models
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializers import *

__all__ = ('ComponentViewset', 'RecordViewset', 'TypeViewset', 'AttrViewset',)


class TypeViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    permission_classes = ()
    serializer_class = TypeSerializer
    queryset = Type.objects.all()
    filterset_fields = ('name',)
    search_fields = ('name', 'id')


class AttrViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    permission_classes = ()
    serializer_class = AttrSerializer
    queryset = Attr.objects.all()
    filterset_fields = ('name',)
    search_fields = ('name', 'id')


class ComponentViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    permission_classes = ()
    serializer_class = ComponentSerializer
    queryset = Component.objects.all()
    filterset_fields = ('types', 'attrs',)
    search_fields = ('name', 'id', )

    @action(['get'], False)
    def sum(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.aggregate(
            money=models.Sum('money'), num=models.Sum('num'))
        return Response(data)


class RecordViewset(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    permission_classes = ()
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    filterset_fields = {
        'time': ['date__gte', 'date__lte', 'date__year', 'date__day', 'date__month'],
        'component': ['exact', 'in']}

    @action(['post'], False, url_path='by_raw')
    def create_by_raw(self, request, *args, **kwargs):
        name = request.data.get('component')
        if not name:
            return Response({'detail': '缺少component'}, status=status.HTTP_400_BAD_REQUEST)
        com = Component.objects.get_or_create(name=name)[0]
        request.data['component'] = com.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(['get'], False)
    def sum(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        input = queryset.filter(operation=1)
        output = queryset.filter(operation=-1)
        data = {
            'input': input.aggregate(
                money=models.Sum('money'), num=models.Sum('num')),
            'output': output.aggregate(
                money=models.Sum('money'), num=models.Sum('num')), }
        return Response(data)

    @action(['get'], False)
    def by_month(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        input = queryset.filter(operation=1).values('time__month')
        output = queryset.filter(operation=-1).values('time__month')
        data = {
            'input': input.values('time__year', 'time__month').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
            'output': output.values('time__year', 'time__month').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
        }
        return Response(data)

    @action(['get'], False)
    def by_week(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        input = queryset.filter(operation=1).values('time__month')
        output = queryset.filter(operation=-1).values('time__month')
        data = {
            'input': input.values('time__year', 'time__week').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
            'output': output.values('time__year', 'time__week').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
        }
        return Response(data)

    @action(['get'], False)
    def by_day(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        input = queryset.filter(operation=1).values('time__month')
        output = queryset.filter(operation=-1).values('time__month')
        data = {
            'input': input.values('time__year', 'time__month', 'time__day').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
            'output': output.values('time__year', 'time__month', 'time__day').annotate(
                money=models.Sum('money'), num=models.Sum('num')),
        }
        return Response(data)
