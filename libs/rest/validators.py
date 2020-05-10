from rest_framework.validators import (
    ValidationError, UniqueTogetherValidator, qs_exists)
from django.core.validators import _, _lazy_re_compile


class RegexValidator:
    regex = ''
    message = _('Enter a valid value.')
    code = 'invalid'
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None, flags=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags
        if self.flags and not isinstance(self.regex, str):
            raise TypeError(
                "If the flags are set, regex must be a regular expression string.")

        self.regex = _lazy_re_compile(self.regex, self.flags)

    def __call__(self, value):
        """
        Validate that the input contains (or does *not* contain, if
        inverse_match is True) a match for the regular expression.
        """
        regex_matches = self.regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, RegexValidator) and
            self.regex.pattern == other.regex.pattern and
            self.regex.flags == other.regex.flags and
            (self.message == other.message) and
            (self.code == other.code) and
            (self.inverse_match == other.inverse_match)
        )


class RelatedToOwnValidator:
    def __init__(self, m2m=False, to_owner_field='owner'):
        self.m2m = m2m
        self.to_owner_field = to_owner_field

    requires_context = True

    def __call__(self, data, serializer_field):
        from_owner = getattr(
            serializer_field.parent.context['request'], 'user')
        if self.m2m:
            for i in data:
                if getattr(i, self.to_owner_field) != from_owner:
                    raise ValidationError('不允许关联他人的%s' %
                                          serializer_field.source_attrs[-1])
        else:
            if getattr(data, self.to_owner_field) != from_owner:
                raise ValidationError('不允许关联他人的%s' %
                                      serializer_field.source_attrs[-1])


class M2MNumValidator:
    def __init__(self, max_num=None, min_num=None):
        self.max_num = max_num
        self.min_num = min_num

    requires_context = True

    def __call__(self, data, serializer_field):
        num = len(data)
        if self.min_num is not None:
            if num < self.min_num:
                raise ValidationError('%s关联不得少于%d个' % (
                    serializer_field.source_attrs[-1], self.min_num))
        if self.max_num is not None:
            if num > self.max_num:
                raise ValidationError('%s关联不得多于%d个' % (
                    serializer_field.source_attrs[-1], self.max_num))


class RecursiveRelationValidator():
    def __init__(self, m2o_field='parent'):
        self.m2o_field = m2o_field

    requires_context = True

    def __call__(self, data, serializer):
        instance = getattr(serializer, 'instance', None)
        parent = data[self.m2o_field]
        if parent is None:
            return
        # 创建时instance为None, 这时也不可能关联到本身
        if instance is not None:
            if instance.id == parent.id:
                raise ValidationError('不允许关联本身')
