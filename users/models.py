from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    def __str__(self):
        return f'{self.username}'


class OneTimeCode(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} - {self.user}'
