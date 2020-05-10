from rest_framework import permissions as drf
from functools import wraps
from types import MethodType


def isOwnerOrReadOnly(field='owner'):
    def foo(self, request, view, obj):
        if request.method in drf.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and eval('obj.%s == request.user' % field))
    return type('IsOwnerOrReadOnly', (drf.IsAuthenticatedOrReadOnly, drf.BasePermission, ), {'has_object_permission': foo})


class IsOwnerOrReadOnly(drf.IsAuthenticatedOrReadOnly, drf.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in drf.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
