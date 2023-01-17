"""Django ORM app posts."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Table for groups."""

    title = models.CharField(
        'Заголовок',
        help_text='Введите название группы',
        max_length=200,
    )
    slug = models.SlugField(unique=True)
    description = models.TextField(
        'Описание',
        help_text='Введите описание группы',
    )

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Table for posts."""

    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )

    class Meta:
        """Sorted all posts by date."""

        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]
