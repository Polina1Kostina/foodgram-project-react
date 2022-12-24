from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователи"""
    USER = 'user'
    ADMIN = 'admin'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    ROLE_CHOISES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        'username',
        max_length=150,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        'last_name',
        max_length=150,
        blank=False
    )
    email = models.EmailField(
        'email address',
        blank=False,
        unique=True
    )

    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER


class Subscription(models.Model):
    """Подписки на пользователей"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='subscrib'
    )
    subscription = models.ForeignKey(
        User,
        verbose_name='Подписка',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'subscription'), name='unique subscription'
            )
        ]
