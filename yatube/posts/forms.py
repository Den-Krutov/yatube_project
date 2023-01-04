from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        labels = {
            'text': _('Текст поста'),
            'group': _('Группа'),
        }
        help_texts = {
            'text': _('Текст нового поста'),
            'group': _('Группа, к которой будет относиться пост'),
        }

    MAX_LENGTH_TEXT = 2048
    MAX_LENGTH_WORD = 64

    def clean_text(self):
        data = self.cleaned_data["text"]
        if len(data) > self.MAX_LENGTH_TEXT:
            raise forms.ValidationError(
                '%(value)s',
                code='max_length_text',
                params={'value': _('Пост слишком большой')}
            )
        for word in data.split():
            if len(word) > self.MAX_LENGTH_WORD:
                raise forms.ValidationError(
                    '%(value)s',
                    code='max_length_word',
                    params={'value': _('В записи присутствует '
                                       'слишком большое слово')}
                )
        return data
