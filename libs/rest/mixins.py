from rest_framework import mixins as drf
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    one_included = one_excluded = ()

    def retrieve(self, request, *args, **kwargs):
        # QueryDict().getlist(key, default=None)
        # 坑: 默认的(default=None时)返回值为[]
        included = set(
            self.one_included or request.query_params.getlist('included'))
        excluded = set(request.query_params.getlist(
            'excluded')) | set(self.one_excluded)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,  included=included, excluded=excluded)
        return drf.Response(serializer.data)


class ListModelMixin:
    """
    List a queryset.
    判断是否
    """
    many_included = many_excluded = ()

    def list(self, request, *args, **kwargs):
        included = set(
            self.many_included or request.query_params.getlist('included')) or None
        excluded = set(request.query_params.getlist(
            'excluded')) | set(self.many_excluded or ())
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, included=included, excluded=excluded)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, included=included, excluded=excluded)
        return drf.Response(serializer.data)


class ExistsModelMixin:
    """
    由查询条件判断实例是否存在
    存在返回True, 不存在就创建(POST)
    """
    @action(detail=False, methods=['GET', 'POST', ], url_path='exists', url_name='exists', permission_classes=[IsAuthenticatedOrReadOnly, ])
    def exists(self, request, *args, **kwargs):
        """
        由查询条件判断实例是否存在
        存在返回True, 不存在就创建(POST)
        """
        exists = self.filter_queryset(self.get_queryset()).exists()
        if request.method == 'GET':
            return drf.Response({'exists': exists})
        else:
            if exists:
                return drf.Response({'exists': True})
            return self.create(request, *args, **kwargs)
