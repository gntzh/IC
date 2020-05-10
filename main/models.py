from django.db import models
from django.utils import timezone


class Attr(models.Model):
    name = models.CharField('名称', max_length=64, unique=True)

    class Meta:
        verbose_name = '属性'
        verbose_name_plural = verbose_name
        default_related_name = 'attrs'

    def __str__(self):
        return "<Attr(%s):%s>" % (self.id, self.name[:8])


class Type(models.Model):
    name = models.CharField('名称', max_length=64, unique=True)

    class Meta:
        verbose_name = '类型'
        verbose_name_plural = verbose_name
        default_related_name = 'types'

    def __str__(self):
        return "<Type(%s):%s>" % (self.id, self.name[:8])


class Component(models.Model):
    name = models.CharField('名称', max_length=128, unique=True)
    types = models.ManyToManyField(
        Type, related_query_name='component', verbose_name='类型')
    attrs = models.ManyToManyField(
        Attr, related_query_name='component', verbose_name='属性')

    num = models.IntegerField('数量', default=0)
    money = models.FloatField('价值总额', default=0)

    min_num = models.IntegerField('库存下限', default=10)

    class Meta:
        verbose_name = '元器件'
        verbose_name_plural = verbose_name
        default_related_name = 'components'

    def __str__(self):
        return "<%s:%s>" % (self.id, self.name[:16])


class Record(models.Model):
    OPERATIONS = (
        (1, '入库'),
        (-1, '出库')
    )
    operation = models.IntegerField('操作', choices=OPERATIONS)
    component = models.ForeignKey(
        Component, models.CASCADE, related_query_name='recore')
    num = models.IntegerField('交易数量', default=0)
    money = models.FloatField('交易金额', default=0)
    time = models.DateTimeField('交易时间', default=timezone.now)


    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name
        default_related_name = 'records'

    def __str__(self):
        return "<Record(%s):%s>" % (self.id, self.get_operation_display())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.component.num += self.operation * self.num
            self.component.money += self.operation * self.money
            self.component.save()
        super().save(*args, **kwargs)


__all__ = ('Attr', 'Type', 'Component', 'Record')
