from django import forms
from .models import Comment

BAD_WORDS = ['запрещённое_слово', 'spam', 'offensive']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data.get('text', '').lower()
        for word in BAD_WORDS:
            if word.lower() in text:
                raise forms.ValidationError(
                    'Комментарий содержит запрещённые слова.'
                )
        return text
