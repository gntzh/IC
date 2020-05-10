from django.contrib import admin

from .models import *


@admin.register(Attr)
class AttrAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'num')
    list_filter = ('types', )
    # raw_id_fields = ('types', 'attrs')
    search_fields = ('name',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation', 'component')
    list_filter = ('component', 'operation', )
