from django import forms

from .models import Comment, Post


def _text_validation(text):
    max_length_text = 2048
    max_length_word = 64
    error_messages = {
        'max_length_text': 'Пост слишком большой',
        'max_length_word': 'В записи присутствует слишком большое слово',
    }
    if len(text) > max_length_text:
        raise forms.ValidationError(
            error_messages['max_length_text'],
            code='max_length_text'
        )
    for word in text.split():
        if len(word) > max_length_word:
            raise forms.ValidationError(
                error_messages['max_length_word'],
                code='max_length_word'
            )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        text = self.cleaned_data['text']
        _text_validation(text)
        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        _text_validation(text)
        return text
