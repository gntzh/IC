from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # uid = models.UUIDField(default=uuid.uuid4, editable=False)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    avatar = models.URLField(blank=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", blank=True)
    email = models.EmailField(
        _('email address'), null=True, blank=True, unique=True,)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    email_is_active = models.BooleanField(verbose_name='邮箱状态', default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    sign = models.CharField(max_length=128, verbose_name='个人签名', blank=True)
    comment_count = models.PositiveIntegerField('留言数', default=0, )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        # 对于进行唯一性约束的string field(空值默认约定为空字符串),强制修改为null
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class OUser(models.Model):
    identity_types = (
        ('gh', 'Github'),
        ('wb', '微博'),
    )
    user = models.ForeignKey(User, models.CASCADE,
                             related_query_name='ouser', verbose_name='站内用户')
    identifier = models.CharField(max_length=256, verbose_name='唯一且不变标识')
    identity_type = models.CharField(
        max_length=2, choices=identity_types, verbose_name='平台')
    # credential

    class Meta:
        verbose_name = '其他用户'
        verbose_name_plural = verbose_name
        default_related_name = 'ousers'
        unique_together = ('identity_type', 'identifier')
