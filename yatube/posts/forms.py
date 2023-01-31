from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    MAX_LENGTH_TEXT = 2048
    MAX_LENGTH_WORD = 64

    error_messages = {
        'max_length_text': 'Пост слишком большой',
        'max_length_word': 'В записи присутствует слишком большое слово',
    }

    class Meta:
        model = Post
        fields = '__all__'

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > self.MAX_LENGTH_TEXT:
            raise forms.ValidationError(
                self.error_messages['max_length_text'],
                code='max_length_text'
            )
        for word in text.split():
            if len(word) > self.MAX_LENGTH_WORD:
                raise forms.ValidationError(
                    self.error_messages['max_length_word'],
                    code='max_length_word'
                )
        return text
